/**
 * Created by hu on 2015/2/13.
 */

var topleft = document.createElement("div");
topleft.className = 'bg topleft';

var topright = document.createElement("div");
topright.className = 'bg topright';

var midleft1 = document.createElement("div");
midleft1.className = 'bg midleft1';

var midright1 = document.createElement("div");
midright1.className = 'bg midright1';

//var midleft2 = document.createElement("div");
//midleft2.className = 'bg midleft2';
//
//var midright2 = document.createElement("div");
//midright2.className = 'bg midright2';

var bottomleft = document.createElement("div");
bottomleft.className = 'bg bottomleft';

var bottomright = document.createElement("div");
bottomright.className = 'bg bottomright';

topleft.appendChild(document.createTextNode(username));
topright.appendChild(document.createTextNode(username));
midleft1.appendChild(document.createTextNode(username));
midright1.appendChild(document.createTextNode(username));
//midleft2.appendChild(document.createTextNode(username));
//midright2.appendChild(document.createTextNode(username));
bottomleft.appendChild(document.createTextNode(username));
bottomright.appendChild(document.createTextNode(username));

document.body.appendChild(topleft);
document.body.appendChild(topright);
document.body.appendChild(midleft1);
document.body.appendChild(midright1);
//document.body.appendChild(midleft2);
//document.body.appendChild(midright2);
document.body.appendChild(bottomleft);
document.body.appendChild(bottomright);
