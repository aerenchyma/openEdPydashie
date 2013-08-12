<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="description" content="">
  <meta name="viewport" content="width=device-width">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title>{{title}}</title>

  <!-- The javascript and css are managed by sprockets. The files can be found in the /assets folder-->
  <script type="text/javascript" src="/assets/application.js"></script>
  <script type="text/javascript" src="../javascripts/jquery.js"></script>
  <link rel="stylesheet" href="/assets/application.css">

  <link href='http://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700' rel='stylesheet' type='text/css'>
  <link rel="icon" href="/assets/images/favicon.ico">




</head>

<script type="text/javascript">
  list = document.getElementById("widgetlist");


  //var kid = list.children[0];
  function generate(choosecourse) {
    //if (choosecourse.preventDefault) choosecourse.preventDefault();
    //window.list = document.getElementById("widgetlist");
    //alert("function!");
    //alert(choosecourse);
    //alert(document.getElementById("testform").value);
    //var elem = document.getElementById("testform");
    //alert(elem.choosecourse.length);
    //alert(elem.choosecourse.options[elem.choosecourse.selectedIndex].value);
    //document.write('<p>hello </p>');
    // var list = document.getElementById("widgetlist");
    // var li = document.createElement('li');
    // var p = document.createElement('p');
    // var t = document.createTextNode("TEST LIST ITEM");
    // p.appendChild(t);
    // li.appendChild(p);
    // list.appendChild(li);
    //var list = document.getElementById("widgetlist");
    //list.children[0].outerHTML = "hello world";
    //window.list.children[0].innerHTML="hello world";
    //$.event.preventDefault();
    //document.getElementById("widgetlist").appendChild(node);
    //$('<li data-row="3" data-col="1" data-sizex="1" data-sizey="1"><div data-id="convergence" data-view="Graph" data-title="Downloads over other months" style="background-color:#3385FF"></div></li>').appendTo("#widgetlist");
    //list.appendChild(' <li data-row="3" data-col="1" data-sizex="1" data-sizey="1"><div data-id="convergence" data-view="Graph" data-title="Downloads over other months" style="background-color:#3385FF"></div></li>');
    //alert("checking"); 
    //kid.innerHTML = "NEW hello world";
    alert("is this working?");
    list.children[0].innerHTML = "NEW hello world";
    alert(list.children[0].innerHTML);
    //return false;
  }

  // var form = document.getElementById('testform');
  // if (form.attachEvent) {
  //   form.attachEvent("submit", generate);
  // } else {
  //   form.addEventListener("submit", generate);
  // }
</script>


  <body>
    <div id="container">
      <div class="gridster">
  <ul id="widgetlist">
    <li data-row="1" data-col="1" data-sizex="1" data-sizey="1">
      <div data-id="welcome" data-view="Text" data-title="Welcome to Open.Michigan's" data-text="Dynamic Metrics dashboard" data-moreinfo="Here's info for the past 60 days. Click <u><a alt='click this link to generate a pdf summary of course page metrics' href='http://google.com' target=_blank>here</a></u> to get a PDF summary." style="background-color:#5C85AD"></div>
    </li>
    <!-- clicking that "here" link must enable CGI script and bring up window (???) for download, or just d/l. Problem: getting accurate path for this and also for PDF via cgi. How does it connect?? -->


    <li data-row="1" data-col="1" data-sizex="1" data-sizey="1">
      <div data-id="synergy" data-view="Meter" data-title="Synergy" data-min="0" data-max="100"></div>
          <p><form name="testform" id="testform" action="" >
        Choose a course: <br />
        <select name="choosecourse">
        <option value="" selected="selected">None Selected</option>
        <option value="7402">General Physics 1</option>
        <option value="1048">Networks</option>
        </select>
        <input type="submit" value="Submit" onclick="generate()">
      </form>
      </p>
    </li> 




   <!-- <li data-row="1" data-col="1" data-sizex="1" data-sizey="1">
      <div data-id="buzzwords" data-view="List" data-unordered="true" data-title="Global reach" data-moreinfo=""></div>
    </li> -->

    <!-- added this -->
    <!-- <li data-row="1" data-col="1" data-sizex="1" data-sizey="1">
      <div data-id="secbuzzwords" data-view="List" data-unordered="true" data-title="City spread" data-moreinfo="" style="background-color:#33CCCC"></div>
    </li> --> <!-- need to fix for correct data in these different data same widgets business -->

 
    <li data-row="2" data-col="1" data-sizex="1" data-sizey="1">
      <div data-id="convergence" data-view="Graph" data-title="Downloads over past 2 months" style="background-color:#3385FF"></div>
    </li>

    <li data-row="2" data-col="2" data-sizex="1" data-sizey="1">
      <div data-id="sec_convergence" data-view="Graph" data-title="Views over past 2 months" style="background-color:#9bcd9b"></div>
    </li>

    <li data-row="2" data-col="3" data-sizex="1" data-sizey="1">
      <div data-id="youtubestats" data-view="List" data-unordered="true" data-title="YouTube metrics" data-moreinfo="for content associated with this course" style="background-color:#003b6f"></div>
    </li>

    <li data-row="2" data-col="4" data-sizex="1" data-sizey="1">
      <div data-id="<a href=''>test link</a>" data-view="Number" data-title="<a href=''>test link</a>" data-moreinfo="<a href=''>test</a>" style="background-color:#003b6f">
    </div>
    </li>

  </ul>
    </div>
  </body>
</html>


