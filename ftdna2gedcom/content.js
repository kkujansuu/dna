// ==UserScript==
// @name FTDNA family tree to Gedcom
// @include https://www.familytreedna.com/my/family-tree/*
// @require jquery-1.9.1.min.js
// ==/UserScript==

var $ = window.$.noConflict(true); 

function log(msg) {
    console.log(msg);
}

var name;
var gedcomdiv;
var people = {};
var num_people = 0;
var todo = [];
var families = {};
var family_list = [];
var next_fam_id = 1;
var done = {};
var kitnum;
var gedcom = "";
var starttime;
var fetches = 0;
var persons_fetched = 0;

function progress() {
    num_people ++;
    // $("#gedcom").text("Gedcom in progress: " + num_people + " people");
    $("#gedcom-button").val("Gedcom in progress: " + num_people + " people");
}

function getName(person) {
    var fn = fixname(person.person.firstName);
    var mn = fixname(person.person.middleName);
    fn = (fn + " " + mn).trim();
    var ln = fixname(person.person.lastName);
    return (fn + " " + ln).trim();
}    

function add_person(person) {
   if (person.id in people) {
        log("already added: " + person.id  + ": " + getName(person));
        return;
    }
    persons_fetched++;
    progress();
    log("adding person " + person.id + ": " + getName(person));
    people[person.id] = person;
    person.fams = [];
    person.famc = null;
}

function process_person(person) {
    if (done[person.id]) {
        log("already done: " + person.id + ": " + getName(person));
        return;
    }
    person = people[person.id];
    var father_id = person.fatherId;
    var mother_id = person.motherId;
    var spouse_id = person.spouseId;
    var father = null;
    var mother = null;
    var spouse = null;
    if (father_id) {
        father = people[father_id];
        if (!father) {
            if (todo.indexOf(father_id) == -1) todo.push(father_id);
        }
    }
    if (mother_id) {
        mother = people[mother_id];
        if (!mother) {
            if (todo.indexOf(mother_id) == -1) todo.push(mother_id);
        }
    }
    if (spouse_id) {
        spouse = people[spouse_id];
        if (!spouse) {
            if (todo.indexOf(spouse_id) == -1) todo.push(spouse_id);
        }
    }

    done[person.id] = true;
}

function add_data(p_id,rsp) {
    log("len rsp="+rsp.length);
    $.each(rsp, function(i,p) {
        add_person(p);
    });
    $.each(rsp, function(i,p) {
        process_person(p);
    });
}


function emit(line) {
    // log("emitting " + line);
    gedcom += line+"\r\n";
}

//https://www.familytreedna.com/my/family-tree/getTreePeople?startId=&pedigreeView=false&generationCount=4&alwaysIncludeTreeOwner=true&treeKitNum=vHbc7LK8srGqJ30YrwG+5g==&_=1449852816936

function fetch() {        
    var p_id = todo.shift()
    log("fetching " + p_id);
    //var url = "https://my.familytreedna.com/family-tree/getTreePeople?startId=" + p_id;
    var url = "https://www.familytreedna.com/my/family-tree/getTreePeople?startId=" + p_id;
    url += "&pedigreeView=true&generationCount=15&treeKitNum=" + kitnum;
    fetches++;
    $.get(url, function(rsp) {
        add_data(p_id,rsp);
        if (todo.length > 0) 
            fetch();
        else
            output_gedcom();
    });
}

function generate_gedcom() {        
    starttime = new Date();
    $("#gedcom-button").val("Gedcom in progress");
    var elem = $("div.tree-owner[id]");
    name = $("div.name",elem).attr("title");
    log("name="+name);
    var p_id;
    $.each(elem,function(i,e) {
        var id = $(e).attr("data-id");
        var id1 = $(e).attr("id");
        log("\nid="+id+" id1="+id1);
        if (id) p_id = id;
    });
    var page_url = document.location.href;  // eg. https://my.familytreedna.com/family-tree/share?k=7Z1I%2bbawZMsGMZpsSrSpJQ%3d%3d
    kitnum = page_url.split("=")[1];

    todo = [p_id];
    fetch();
}

function datestring(yy,mm,dd) {
    var d = new Date(yy,mm-1,dd);
    s = d.toDateString();
    var x = s.split(" ");
    var ds = x[2] + " " + x[1] + " " + x[3];
    return ds.toUpperCase();
}

function getdate(year,month,day) {
    if (year && month && day) {
        var s = datestring(year,month,day);
        return s;
    }
    if (year) {
        return "" + year;
    }
    return "";
}


function getbirthdate(person) {
    var details = person.person;
    return getdate(details.birthYear,details.birthMonth,details.birthDay);
}
    
function getdeathdate(person) {
    var details = person.person;
    return getdate(details.deathYear,details.deathMonth,details.deathDay);
}

function fixname(s) {    
    if (!s) return "";
    s = s.replace(/Ã¤/g,"ä"); 
    s = s.replace(/Ã¶/g,"ö"); 
    
    return s;
}

function output_gedcom() {        
    log("writing gedcom");
    emit("0 HEAD");
    emit("1 CHAR UTF-8")
    //emit("1 CHAR ISO8859-1")

    // build families
    $.each(people,function(i,person) {
        if (person.fatherId || person.motherId) {
            var fam_key = person.fatherId+"+"+person.motherId;
            var family = families[fam_key];
            if (!family) {
                family = new Object(); // {father:father_id,mother:mother_id,children:new Array(),id:next_fam_id};
                family.father = person.fatherId;
                family.mother = person.motherId;
                family.children = new Array()
                family.id = next_fam_id;
                next_fam_id += 1;
                families[fam_key] = family;
                var father = people[person.fatherId];
                var mother = people[person.motherId];
                if (father) father.fams.push(family.id);
                if (mother) mother.fams.push(family.id);
                family_list.push(family);
            }
            person.famc = family.id;
            family.children.push(person.id);
        }
    });


    $.each(people,function(i,person) {
        emit("0 @" + person.id + "@ INDI")
        var fn = fixname(person.person.firstName);
        var mn = fixname(person.person.middleName);
        fn = (fn + " " + mn).trim();
        var ln = fixname(person.person.lastName);
        emit("1 NAME " + fn + " /" + ln + "/")
        if (fn) emit("2 GIVN " + fn);
        if (ln) emit("2 SURN " + ln);
        if (person.person.gender) emit("1 SEX " + person.person.gender);
        
        var d = getbirthdate(person);
        if (d) {
            emit("1 BIRT");
            emit("2 DATE " + d);
            if (person.person.birthPlace) 
                emit("2 PLAC " + fixname(person.person.birthPlace));
        }
        else if (person.person.birthPlace) {
            emit("1 BIRT");
            emit("2 PLAC " + fixname(person.person.birthPlace));
        }
        
        d = getdeathdate(person);
        if (d) {
            emit("1 DEAT");
            emit("2 DATE " + d);
            if (person.person.deathPlace) 
                emit("2 PLAC " + fixname(person.person.deathPlace));
        }
        else if (person.person.deathPlace) {
            emit("1 DEAT");
            emit("2 PLAC " + fixname(person.person.deathPlace));
        }

        $.each(person.fams,function(j,fam_id) {
            emit("1 FAMS @" + fam_id + "@");
        });
        if (person.famc) emit("1 FAMC @" + person.famc + "@");
    });
    $.each(family_list,function(i,fam) {
        emit("0 @" + fam.id + "@ FAM");
        if (fam.father) emit("1 HUSB @" + fam.father + "@");
        if (fam.mother) emit("1 WIFE @" + fam.mother + "@");
        $.each(fam.children,function(j,child_id) {
            emit("1 CHIL @" + child_id + "@");
        });
    });
    emit("0 TRLR");

    // from http://stackoverflow.com/questions/3665115/create-a-file-in-memory-for-user-to-download-not-through-server
    var a = window.document.createElement('a');
    a.href = window.URL.createObjectURL(new Blob([gedcom], {type: 'text/csv'}));
    var dt = new Date();
    var datestring = dt.toISOString().substring(0,10);
    a.download = "FTDNA " + name + " " + datestring + ".ged";

    // Append anchor to body.
    document.body.appendChild(a)
    a.click();

    // Remove anchor from body
    document.body.removeChild(a)

    $("#gedcom-button").val("Generate GEDCOM");
    var endtime = new Date();
    log("num people: " + num_people);
    log("fetches: " + fetches);
    log("persons fetched: " + persons_fetched);
  
    log("Start time: " + starttime);
    log("End   time: " + endtime);
    log("Elapsed time: " + (endtime.getTime() - starttime.getTime())/1000 + " s");

};

$(document).ready( function() {        
    $(document).ajaxError(function(e, xhr, settings, exception) {
        alert('error in:\n- ' + settings.url + '\n'+'error:\n- ' + exception);
        $("#gedcom-button").val("Generate GEDCOM");
    });        

    var but = $("<input type=button id=gedcom-button class='btn btn-mellowyellow' value='Generate GEDCOM'/>");
    but.css("position","absolute").css("top","57px").css("left","250px"); // .css("z-index",999);
    but.click(generate_gedcom);
    $("body").append(but);
});

