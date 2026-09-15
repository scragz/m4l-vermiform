"""Build editable sources and an unfrozen staging AMXD; final is saved/frozen in Max."""
from pathlib import Path
import json,struct,shutil
from tables import write as tables
ROOT=Path(__file__).resolve().parents[1];DEST=ROOT/'scripts/build';DEST.mkdir(exist_ok=True)
V=dict(major=9,minor=0,revision=9,architecture='x64',modernui=1)
B=[];L=[];P={}
BG=[.065,.08,.065,1];INK=[.91,.91,.84,1];ACID=[.71,.84,.31,1];RUST=[.88,.43,.28,1]
def box(id,cls,rect,**kw):B.append({'box':dict(id=id,maxclass=cls,patching_rect=rect,**kw)});return id
def obj(id,text,x,y,ni=1,no=1,**kw):return box(id,'newobj',[x,y,210,22],text=text,numinlets=ni,numoutlets=no,**kw)
def wire(a,b,o=0,i=0):L.append({'patchline':dict(source=[a,o],destination=[b,i])})
def parameter(key,label,lo,hi,val,rect=None,cls='live.dial',enum=None,**kw):
 i=len(P);attr=dict(parameter_longname=label,parameter_shortname=label,parameter_type=2 if enum else (1 if key=='mode' else 0),parameter_mmin=lo,parameter_mmax=hi,parameter_initial=[val],parameter_initial_enable=1,parameter_unitstyle=0)
 if enum:attr.update(parameter_enum=enum,parameter_unitstyle=9)
 if key=='output':attr['parameter_unitstyle']=4
 box(key,cls,[20+i%8*140,400+i//8*100,60,48],varname=key,parameter_enable=1,saved_attribute_attributes={'valueof':attr},numinlets=1,numoutlets=3 if cls=='live.menu' else 2,**(dict(presentation=1,presentation_rect=rect) if rect else {}),**kw)
 P[key]=[label,label,0];obj('p-'+key,'prepend '+key,20+i%8*140,450+i//8*100);wire(key,'p-'+key);wire('p-'+key,'control')
def dial(key,label,lo,hi,val,x,y,color=ACID):parameter(key,label,lo,hi,val,[x,y,66,58],activefgdialcolor=color,activeneedlecolor=INK,activedialcolor=[.22,.28,.20,1],textcolor=INK,textcolor2=INK,fontsize=10)
def button(key,label,rect):parameter(key,label,0,1,0,rect,cls='live.text',enum=['Off','On'],text=label,texton=label,mode=1,fontsize=9,bgcolor=[.17,.22,.14,1],bgoncolor=ACID,textcolor=INK,textoncolor=BG,rounded=3)
def action(key,label,rect):
 box(key,'textbutton',[1200,len(B)*25,90,22],varname=key,presentation=1,presentation_rect=rect,text=label,texton=label,mode=0,numinlets=1,numoutlets=3,bgcolor=[.22,.27,.18,1],textcolor=INK,fontsize=9,rounded=3)
 obj('a-'+key,'sel 1',1400,len(B)*25);box('m-'+key,'message',[1600,len(B)*25,90,22],text=key);wire(key,'a-'+key);wire('a-'+key,'m-'+key);wire('m-'+key,'control')
def gen(code):
 bs=[{'box':dict(id='code',maxclass='codebox',code=code,numinlets=1,numoutlets=6,patching_rect=[20,70,850,650])}];ls=[]
 for i in range(6):bs.append({'box':dict(id=f'out{i}',maxclass='newobj',text=f'out {i+1}',patching_rect=[20+i*110,750,70,22])});ls.append({'patchline':dict(source=['code',i],destination=[f'out{i}',0])})
 return dict(fileversion=1,appversion=V,classnamespace='dsp.gen',rect=[0,0,900,820],boxes=bs,lines=ls)
D=tables(ROOT/'src');(ROOT/'src/vermiform.tables.json').write_text(json.dumps(D,indent=2)+'\n')
js='var TABLES='+json.dumps(D,separators=(',',':'))+';\n'+(ROOT/'src/vermiform.control.js').read_text()
(DEST/'vermiform.control.js').write_text(js)
for n in ['vermiform.panel.js','vermiform.segments.wav']:shutil.copyfile(ROOT/'src'/n,DEST/n)
box('panel','jsui',[0,0,1100,169],varname='panel',filename='vermiform.panel.js',presentation=1,presentation_rect=[0,0,1100,169],numinlets=1,numoutlets=1,border=0,ignoreclick=1)
obj('control','js vermiform.control.js',20,850,no=2,varname='control');wire('control','panel',1)
for key,items,rect in [('corepicker',['Speak & Worm','Intelliworm','Vermis','Saw','Digiwormer','Wormant','Compost'],[14,48,226,21]),('subpicker',[str(x['mode'])+'  '+x['name'] for x in D['modes'][:21]],[14,75,226,21])]:
 box(key,'umenu',[20,220 if key=='corepicker' else 250,230,22],varname=key,items=sum(([s,','] for s in items),[])[:-1],presentation=1,presentation_rect=rect,numinlets=1,numoutlets=3,fontsize=11,bgcolor=[.17,.22,.14,1],textcolor=INK)
 obj('p-'+key,'prepend '+('corePick' if key=='corepicker' else 'subPick'),300,220 if key=='corepicker' else 250);wire(key,'p-'+key);wire('p-'+key,'control')
parameter('mode','Mode',1,64,1)
dial('speed','Speed',0,127,64,264,40)
for k,x,v in [('x',338,64),('y',418,48),('z',498,0)]:dial(k,k.upper(),0,127,v,x,40)
button('stretch','1/32',[268,114,58,19]);button('drone','DRONE',[339,114,67,19]);button('armed','ARM',[418,114,65,19]);button('trigger','TRIGGER',[498,114,76,19])
# Momentary UI trigger, while retaining its Live parameter and first macro bank.
next(b['box'] for b in B if b['box']['id']=='trigger')['mode']=0
L[:]=[l for l in L if l['patchline']['source'][0]!='trigger']
box('trigger-msg','message',[1250,400,60,22],text='trigger');wire('trigger','trigger-msg');wire('trigger-msg','control')
action('panic','STOP',[498,139,76,18]);action('speak','SPEAK',[183,126,57,26])
box('textinput','textedit',[20,740,220,45],varname='textinput',presentation=1,presentation_rect=[14,126,164,28],text='the worm speaks',fontsize=11,lines=1,rounded=3,bgcolor=[.13,.17,.10,1],textcolor=INK,keymode=1,outputmode=1,numinlets=1,numoutlets=4)
wire('textinput','control')
# A hidden parameter-enabled pattr stores text and phoneme list in Live's device state.
obj('memory','pattr memory @parameter_enable 1 @initial '+json.dumps(json.dumps({'text':'the worm speaks','list':[46,51,16,4]})),20,950,no=3,varname='memory',saved_attribute_attributes={'valueof':dict(parameter_longname='Speech text and list',parameter_shortname='Speech text',parameter_type=3,parameter_invisible=1)})
obj('restore','prepend restore',250,950);wire('memory','restore');wire('restore','control')
dial('rate','Rate',0,100,0,600,35,RUST);dial('depth','Depth',0,100,35,677,35,RUST)
parameter('operation','Worm operation',0,4,0,[603,105,136,20],cls='live.menu',enum=['Jitter','Frame bleed','Bit rot','Loop lock','Order swap'],fontsize=10,textcolor=INK,bgcolor=[.2,.18,.12,1])
action('corrupt','CORRUPT',[748,47,61,27]);action('clean','RESTORE',[748,84,61,27])
parameter('output','Output',-60,0,-12,[839,124,90,19],cls='live.numbox',fontsize=10,textcolor=INK,bgcolor=[.16,.2,.13,1])
parameter('width','Width',0,100,35,[948,124,69,19],cls='live.numbox',fontsize=10,textcolor=INK,bgcolor=[.16,.2,.13,1])
action('triggerReset','RESET',[1030,124,53,19])
# Use the same phrase-start action from the small reset button.
next(b['box'] for b in B if b['box']['id']=='m-triggerReset')['text']='trigger'
G=gen((ROOT/'src/vermiform.genexpr').read_text());obj('dsp','gen~',300,850,no=6,patcher=G,varname='dsp',outlettype=['signal']*6);wire('control','dsp')
obj('segments','buffer~ #0-segments vermiform.segments.wav',20,1000,no=2)
obj('bind','loadmess segments #0-segments',300,1000);wire('bind','dsp')
obj('scopebuffer','buffer~ #0-scope @samps 2048',300,1040,no=2)
obj('scopebind','loadmess scopes #0-scope',300,1070);wire('scopebind','dsp')
obj('scopepanel','loadmess scope #0-scope',780,1070);wire('scopepanel','panel')
obj('audio','plugout~',300,1120,ni=2,no=2);wire('dsp','audio');wire('dsp','audio',1,1)
for i,key in enumerate(['writepos','readpos','meter','sample']):
 obj('snap-'+key,'snapshot~ '+('4' if key=='sample' else '40'),540+i*140,850);obj('view-'+key,'prepend '+key,540+i*140,890);wire('dsp','snap-'+key,i+2);wire('snap-'+key,'view-'+key);wire('view-'+key,'panel')
obj('notes','notein',20,1050,no=3);obj('note-pack','pack 0 0',20,1080,ni=2);obj('note-msg','prepend note',20,1110);wire('notes','note-pack',1,1);wire('notes','note-pack');wire('note-pack','note-msg');wire('note-msg','control')
obj('cc','ctlin',560,1000,no=3);obj('cc-pack','pack 0 0',560,1030,ni=2);obj('cc-msg','prepend cc',560,1060);wire('cc','cc-pack',1,1);wire('cc','cc-pack');wire('cc-pack','cc-msg');wire('cc-msg','control')
obj('bend','bendin @bendmode 2',780,1000);obj('bend-msg','prepend bend',780,1030);wire('bend','bend-msg');wire('bend-msg','control')
obj('init','live.thisdevice',20,1160,no=3);box('initmsg','message',[240,1160,70,22],text='init');wire('init','initmsg');wire('initmsg','control')
P['parameterbanks']={'0':dict(index=0,name='Vermiform',parameters=['mode','speed','x','y','z','rate','depth','trigger']),'1':dict(index=1,name='Performance',parameters=['drone','armed','stretch','operation','output','width','-','-'])};P['inherited_shortname']=1
patch=dict(fileversion=1,appversion=V,classnamespace='box',rect=[70,90,1120,800],openrect=[0,0,1100,169],devicewidth=1100,openinpresentation=1,bglocked=1,bgcolor=BG,default_fontname='Arial',default_fontsize=11,boxes=B[1:]+B[:1],lines=L,parameters=P,autosave=0,title='Vermiform',dependency_cache=[dict(name=n,type='WAVE' if n.endswith('wav') else 'TEXT',implicit=1) for n in ['vermiform.control.js','vermiform.panel.js','vermiform.segments.wav']])
raw=(json.dumps({'patcher':patch},indent=2)+'\n').encode();(DEST/'Vermiform.maxpat').write_bytes(raw)
payload=raw+b'\0';(DEST/'Vermiform.amxd').write_bytes(b'ampf'+struct.pack('<I',4)+b'iiii'+b'meta'+struct.pack('<II',4,0)+b'ptch'+struct.pack('<I',len(payload))+payload)
(DEST/'vermiform.gendsp').write_text(json.dumps({'patcher':G},indent=2)+'\n')
print('Built',DEST/'Vermiform.amxd')
