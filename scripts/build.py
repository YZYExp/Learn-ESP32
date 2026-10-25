"""Check manuscript and build an EPUB reading edition. Requires Python 3 + Pandoc."""
from pathlib import Path
import json,re,subprocess,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'build';BUILD.mkdir(exist_ok=True)
book=json.loads((ROOT/'book.json').read_text());texts=[];errors=[]
for ch in book['chapters']:
 p=ROOT/ch['source']
 if not p.exists():errors.append(f'missing {p}');continue
 s=p.read_text()
 if s.count('```')%2:errors.append(f'unclosed code fence: {p}')
 for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',s):
  if not (p.parent/target).exists():errors.append(f'missing image: {target}')
 if not re.search(r'https://',s):errors.append(f'no source: {p}')
 if len(re.findall(r'[\u4e00-\u9fff]',s))<900:errors.append(f'too short: {p}')
 s=re.sub(r'(?<!!)\[([^\]]+)\]\(\.\./(examples/[^)]+)\)', lambda m: '`'+m.group(2)+'`', s)
 texts.append(s.replace('../assets/','assets/'))
if errors:raise SystemExit('\n'.join(errors))
intro=(ROOT/'appendices/reading-guide.md').read_text();glossary=(ROOT/'appendices/glossary.md').read_text();sources=(ROOT/'references/sources.md').read_text()
merged=f'---\ntitle: "{book["title"]}"\nsubtitle: "{book["subtitle"]}"\nlang: zh-CN\ndate: "{book["date"]}"\n---\n\n'+intro+'\n\n'+'\n\n'.join(texts)+'\n\n'+glossary+'\n\n'+sources
# Combined manuscript lives in build, so preserve relative asset references there.
(BUILD/'ESP32-Atlas.md').write_text(merged.replace('](assets/','](../assets/'))
# Pandoc receives a root-relative temporary source so packaged images resolve deterministically.
temp=BUILD/'epub-input.md';temp.write_text(merged)
css=ROOT/'scripts/epub.css'
subprocess.run(['pandoc',str(temp),'--from=markdown','--to=epub3','--toc','--toc-depth=1','--split-level=1','--resource-path='+str(ROOT),'--css='+str(css),'-o',str(BUILD/'ESP32-Atlas.epub')],cwd=ROOT,check=True)
temp.unlink()
with zipfile.ZipFile(BUILD/'ESP32-Atlas.epub') as z:
 images=[n for n in z.namelist() if n.startswith('EPUB/media/')]
 xhtml=[n for n in z.namelist() if n.endswith('.xhtml')]
 if len(images)!=24:raise SystemExit(f'Expected 24 packaged images, got {len(images)}')
 if len(xhtml)<24:raise SystemExit('Insufficient chapter documents')
report={'chapters':len(texts),'chinese_characters':len(re.findall(r'[\u4e00-\u9fff]',merged)),'figures':24,'epub_packaged_images':len(images),'code_validation':'static review only; no toolchain compilation or physical board execution','hardware':'ESP32-S3-DevKitC-1; Arduino-ESP32 3.x; confirm actual board and library versions'}
(BUILD/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
