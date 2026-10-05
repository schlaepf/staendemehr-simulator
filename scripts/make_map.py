"""Download swiss-maps canton topology and write simplified SVG paths to data/map.json."""
import json, math, os, urllib.request
here = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(here, '..', 'tmp', 'ch.json')
if not os.path.exists(SRC):
    os.makedirs(os.path.dirname(SRC), exist_ok=True)
    urllib.request.urlretrieve('https://cdn.jsdelivr.net/npm/swiss-maps@4/2024/ch-combined.json', SRC)
t=json.load(open(SRC))
sx,sy=t['transform']['scale']; tx,ty=t['transform']['translate']
arcs=[]
for a in t['arcs']:
    x=y=0; pts=[]
    for dx,dy in a:
        x+=dx;y+=dy; pts.append((x*sx+tx,y*sy+ty))
    arcs.append(pts)
def arc(i):
    return arcs[i] if i>=0 else arcs[~i][::-1]
def ring(idx):
    pts=[]
    for i in idx:
        a=arc(i); pts+= a if not pts else a[1:]
    return pts
k=math.cos(math.radians(46.8))
def proj(p): return (p[0]*k, -p[1])
def dp(pts,eps):
    if len(pts)<3: return pts
    (x1,y1),(x2,y2)=pts[0],pts[-1]
    dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy) or 1e-12
    md=0;mi=0
    for i in range(1,len(pts)-1):
        d=abs(dy*pts[i][0]-dx*pts[i][1]+x2*y1-y2*x1)/n
        if d>md: md=d;mi=i
    if md>eps:
        return dp(pts[:mi+1],eps)[:-1]+dp(pts[mi:],eps)
    return [pts[0],pts[-1]]
raw={}
for g in t['objects']['cantons']['geometries']:
    polys=g['arcs'] if g['type']=='MultiPolygon' else [g['arcs']]
    rings=[ring(r) for p in polys for r in p]
    raw[g['id']]=[[proj(p) for p in r] for r in rings]
minx=min(p[0] for rs in raw.values() for r in rs for p in r)
maxx=max(p[0] for rs in raw.values() for r in rs for p in r)
miny=min(p[1] for rs in raw.values() for r in rs for p in r)
maxy=max(p[1] for rs in raw.values() for r in rs for p in r)
S=1000/(maxx-minx)
out={}
for cid,rs in raw.items():
    d=''
    for r in rs:
        h=len(r)//2
        s=dp(r[:h+1],0.001)[:-1]+dp(r[h:],0.001)
        if len(s)<4: continue
        d+='M'+'L'.join(f"{(x-minx)*S:.1f},{(y-miny)*S:.1f}" for x,y in s)+'Z'
    out[cid]=d
W=1000;H=(maxy-miny)*S
json.dump({'w':W,'h':round(H,1),'paths':out},open(os.path.join(here,'..','data','map.json'),'w'))
print(W,H,sum(len(v) for v in out.values()))
