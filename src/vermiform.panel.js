autowatch=1;inlets=1;outlets=1;
mgraphics.init();mgraphics.relative_coords=0;mgraphics.autofill=0;
var memory=null;
function scope(name){memory=new Buffer(name);}
var mode=1,modeName='Phrase banks',xl='Pitch',yl='Bank',zl='Phrase',type='vocab',phrase='the worm speaks',phone='PA1',lock=0,frozen=0,op='Jitter',rot=0,writepos=0,readpos=0,meter=0,samples=[],count=0;
var ink=[.91,.91,.84,1],muted=[.5,.56,.50,1],acid=[.71,.84,.31,1],rust=[.88,.43,.28,1];
function textAt(t,x,y,size,color){mgraphics.set_source_rgba(color||ink);mgraphics.select_font_face('Arial');mgraphics.set_font_size(size);mgraphics.move_to(x,y);mgraphics.show_text(String(t));}
function line(x,y,w,c){mgraphics.set_source_rgba(c||muted);mgraphics.set_line_width(1);mgraphics.move_to(x,y);mgraphics.line_to(x+w,y);mgraphics.stroke();}
function paint(){
 mgraphics.set_source_rgba(.065,.08,.065,1);mgraphics.rectangle(0,0,1100,169);mgraphics.fill();
 textAt('VERMIFORM',14,25,19,acid);textAt('SPEECH / MEMORY / DECAY',14,40,8,muted);
 [254,590,822].forEach(function(x){mgraphics.set_source_rgba(.22,.28,.20,1);mgraphics.rectangle(x,13,1,143);mgraphics.fill();});
 textAt(('0'+mode).slice(-2)+' / '+type.toUpperCase(),142,25,10,muted);
 textAt(phrase.length>34?phrase.slice(0,33)+'…':phrase,14,115,10,ink);
 textAt('X / '+xl,338,30,10,acid);textAt('Y / '+yl,418,30,10,acid);textAt('Z / '+zl,498,30,10,acid);
 textAt('CLOCK',268,30,9,muted);
 textAt('WORM ENGINE',605,25,11,rust);textAt(lock?'LOOP LOCKED':(rot?'ALTERED MEMORY':'SOURCE INTACT'),605,151,9,rot?rust:muted);
 textAt('COMPOST MEMORY',838,25,10,acid);textAt(frozen?'FROZEN':(mode>=63?'READ / WRITE':'CAPTURING'),985,25,8,frozen?rust:muted);
 textAt(phone,839,112,12,ink);textAt('OUT',1016,111,8,muted);
 var left=839,top=43,w=241,h=48;
 mgraphics.set_source_rgba(.10,.14,.09,1);mgraphics.rectangle(left,top,w,h);mgraphics.fill();
 mgraphics.set_source_rgba(acid);mgraphics.set_line_width(1);for(var i=0;i<240;i++){var x=left+i*w/240,y=top+h*.5-clamp(memory?memory.peek(1,Math.floor(i*2048/240)):(samples[(count+i)%240]||0),-1,1)*h*.48;if(i==0)mgraphics.move_to(x,y);else mgraphics.line_to(x,y);}mgraphics.stroke();
 [writepos,readpos].forEach(function(v,i){mgraphics.set_source_rgba(i?rust:ink);mgraphics.rectangle(left+v*w,top,1,h);mgraphics.fill();});
 mgraphics.set_source_rgba(acid);mgraphics.rectangle(1045,103,35*clamp(meter*5,0,1),5);mgraphics.fill();
 textAt('MIDI: last note / sustain / ±2 st',839,152,9,muted);
}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function labels(n,name,x,y,z,t){mode=n;modeName=name;xl=x;yl=y;zl=z;type=t;mgraphics.redraw();}
function anything(){var a=arrayfromargs(arguments);if(messagename=='phrase')phrase=a.join(' ');if(messagename=='phoneme')phone=a[0];if(messagename=='frozen')frozen=a[0];if(messagename=='worm'){op=a[0];lock=a[1];}if(messagename=='decay')rot=a[0];if(messagename=='writepos')writepos=a[0];if(messagename=='readpos')readpos=a[0];if(messagename=='meter')meter=a[0];if(messagename=='sample'){samples[count%240]=a[0];count=(count+1)%240;}mgraphics.redraw();}
