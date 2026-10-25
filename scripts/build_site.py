"""Build a standalone reading website. No Pandoc, hardware tools or EPUB rebuild."""
import argparse
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit
import zipfile
import markdown
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/site'
class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]
    def handle_data(self,data):
        self.parts.append(data)

def plain(html):
    parser=TextOnly(); parser.feed(html)
    return re.sub(r'\s+',' ',' '.join(parser.parts)).strip()

class RewriteLinks(HTMLParser):
    def __init__(self, source, routes, base):
        super().__init__(convert_charrefs=False)
        self.source=source; self.routes=routes; self.base=base; self.output=[]
    def rewrite(self,value):
        if not value or value.startswith(('#','data:','mailto:','https:','http:')):
            return value
        u=urlsplit(value)
        source=(self.source.parent / unquote(u.path)).resolve()
        suffix=('#'+u.fragment) if u.fragment else ''
        if source in self.routes:
            return self.base+self.routes[source]+suffix
        if source.is_relative_to(ROOT/'assets'):
            return self.base+source.relative_to(ROOT).as_posix()+suffix
        if source.is_file() and source.is_relative_to(ROOT):
            return 'https://github.com/YZYExp/Learn-ESP32/blob/main/'+source.relative_to(ROOT).as_posix()+suffix
        raise ValueError(f'Unresolved content link: {self.source.name}: {value}')
    def handle_starttag(self,tag,attrs):
        values=[]
        for key,value in attrs:
            if key in ('href','src'): value=self.rewrite(value)
            if value is None: values.append(key)
            else: values.append(f'{key}="{escape(value,quote=True)}"')
        if tag=='img':values.extend(['loading="lazy"','decoding="async"'])
        self.output.append('<'+tag+(' '+' '.join(values) if values else '')+'>')
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
    def handle_endtag(self,tag):self.output.append('</'+tag+'>')
    def handle_data(self,data):self.output.append(data)
    def handle_entityref(self,name):self.output.append('&'+name+';')
    def handle_charref(self,name):self.output.append('&#'+name+';')

def render(source,routes,base):
    converter=markdown.Markdown(extensions=['tables','fenced_code','toc','sane_lists'])
    html=converter.convert(source.read_text())
    rewrite=RewriteLinks(source,routes,base); rewrite.feed(html)
    return ''.join(rewrite.output), converter.toc

def page(title, description, body, base, book, reader=False):
    menu='<button class="icon-button mobile-only" data-menu-toggle aria-expanded="false" aria-controls="chapter-nav">目录</button>' if reader else ''
    return f'''<!doctype html>
<html lang="zh-CN" data-base="{escape(base)}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · {escape(book['title'])}</title>
<meta name="description" content="{escape(description,quote=True)}"><meta name="theme-color" content="#f7f5ef">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{base}assets/styles.css">
<script>try{{document.documentElement.dataset.theme=localStorage.getItem('esp32-book-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light')}}catch(e){{}}</script>
<script src="{base}assets/app.js" defer></script></head>
<body class="{'reader' if reader else 'home'}">
<a class="skip-link" href="#main">跳到正文</a><div id="reading-progress" aria-hidden="true"></div>
<header class="site-header"><div class="shell"><a class="brand" href="{base}"><span class="brand-mark">E/</span><span class="brand-name">ESP32 图解读本</span></a>
<nav class="top-nav" aria-label="主导航"><a href="{base}#chapters">全书目录</a><a href="{base}read/sources/">资料来源</a><a href="https://github.com/YZYExp/Learn-ESP32">GitHub ↗</a></nav>
<div class="header-actions">{menu}<button class="icon-button" data-search-open aria-label="搜索全书">搜索 <kbd>⌘ K</kbd></button><button class="icon-button" data-theme-toggle aria-label="切换深浅主题">◐</button></div></div></header>
{body}
<footer class="site-footer shell"><span>ESP32 图解读本 · {escape(book['date'])}</span><span><a href="{base}read/qa/">验证边界</a> · <a href="https://github.com/YZYExp/Learn-ESP32">编辑与反馈 ↗</a></span></footer>
<dialog id="search-dialog" class="search-dialog" aria-labelledby="search-title"><div class="dialog-header"><h2 id="search-title">搜索全书</h2><button class="icon-button" data-search-close aria-label="关闭搜索">关闭 ×</button></div><label class="sr-only" for="search-input">章节、概念或问题</label><input id="search-input" type="search" placeholder="试试 GPIO、传感器、FreeRTOS…" autocomplete="off"><p class="search-hint">输入关键词，查找章节与正文。</p><div id="search-results" aria-live="polite"></div></dialog>
<dialog id="image-dialog" class="image-dialog" aria-label="查看原图"><button class="icon-button" data-image-close aria-label="关闭原图">关闭 ×</button><img alt=""><p></p></dialog>
</body></html>'''

def check_links(base):
    errors=[]; pages=list(OUT.rglob('*.html')); parsed={}
    class Collector(HTMLParser):
        def __init__(self):super().__init__();self.links=[];self.ids=set()
        def handle_starttag(self,tag,attrs):
            a=dict(attrs)
            if a.get('id'):self.ids.add(a['id'])
            for key in ('href','src'):
                if a.get(key):self.links.append(a[key])
    for file in pages:
        p=Collector();p.feed(file.read_text());parsed[file]=p
    for file,p in parsed.items():
        for link in p.links:
            u=urlsplit(link)
            if u.scheme or u.netloc:continue
            path=unquote(u.path)
            if not path:target=file
            elif path.startswith(base):target=OUT/path[len(base):]
            elif path.startswith('/'):
                errors.append(f'Wrong base path: {file}: {link}');continue
            else:target=(file.parent/path).resolve()
            if target.is_dir():target=target/'index.html'
            if not target.is_file():errors.append(f'Missing: {file.relative_to(OUT)}: {link}')
            elif u.fragment and target in parsed and unquote(u.fragment) not in parsed[target].ids:
                errors.append(f'Missing fragment: {file.relative_to(OUT)}: {link}')
    if errors:raise ValueError('\n'.join(errors))
    print(f'Checked {len(pages)} HTML pages: local resources and fragments pass.')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-path',default='/Learn-ESP32/')
    args=parser.parse_args()
    base='/'+args.base_path.strip('/')+'/' if args.base_path.strip('/') else '/'
    book=json.loads((ROOT/'book.json').read_text())
    docs=[dict(title='导读与实验边界',source='appendices/reading-guide.md',slug='reading-guide')]+book['chapters']+[
      dict(title=title,source=source,slug=slug) for title,source,slug in [
        ('术语与实验记录','appendices/glossary.md','glossary'),
        ('参考资料索引','references/sources.md','sources'),
        ('本版检查与验证边界','QA.md','qa')]]
    assert len({c['slug'] for c in docs})==len(docs), 'Duplicate routes'
    routes={(ROOT/c['source']).resolve():'read/'+c['slug']+'/' for c in docs}
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT/'assets',OUT/'assets')
    for name in ['styles.css','app.js','favicon.svg']:shutil.copyfile(ROOT/'site'/name,OUT/'assets'/name)
    epub=ROOT/'editions/ESP32-Atlas.epub'
    with zipfile.ZipFile(epub) as z:
        assert z.testzip() is None, 'Damaged EPUB'
        assert z.read('mimetype')==b'application/epub+zip', 'Invalid EPUB'
    (OUT/'downloads').mkdir()
    shutil.copyfile(epub,OUT/'downloads/ESP32-Atlas.epub')
    search=[]
    for index,c in enumerate(docs):
        html,toc=render(ROOT/c['source'],routes,base);text=plain(html)
        links=''.join(f'<li><a href="{base}read/{n["slug"]}/"'+(' class="active" aria-current="page"' if n==c else '')+f'>{escape(n["title"])}</a></li>' for n in docs)
        nav=f'<aside id="chapter-nav" class="chapter-nav" aria-label="全书目录"><a class="nav-heading" href="{base}#chapters">全书目录</a><div class="nav-part"><ol>{links}</ol></div></aside>'
        pagination=''
        for label,pos in [('上一篇',index-1),('下一篇',index+1)]:
            if 0<=pos<len(docs):
                n=docs[pos];pagination+=f'<a href="{base}read/{n["slug"]}/"><small>{label}</small><strong>{escape(n["title"])}</strong></a>'
        body=f'<main id="main" class="reader-grid shell">{nav}<div class="reading-pane"><div class="reading-meta"><a href="{base}">首页</a><span>ESP32 · 图解读本</span></div><article class="prose">{html}</article><nav class="chapter-pagination" aria-label="章节翻页">{pagination}</nav></div><aside class="page-toc" aria-label="本页目录"><strong>本页目录</strong>{toc}</aside></main>'
        target=OUT/'read'/c['slug'];target.mkdir(parents=True)
        (target/'index.html').write_text(page(c['title'],text[:150],body,base,book,True))
        search.append(dict(title=c['title'],url=base+routes[(ROOT/c['source']).resolve()],text=text))
    groups=''
    for title,first,last in [('建立共同语言',1,6),('外设与连接',7,14),('长期运行的系统',15,20),('项目与下一步',21,24)]:
        rows=''.join(f'<a class="chapter-row" href="{base}read/{c["slug"]}/"><span class="chapter-number">{i:02}</span><span class="chapter-summary"><h4>{escape(c["title"])}</h4></span><span class="chapter-meta">阅读 ↗</span></a>' for i,c in enumerate(book['chapters'],1) if first<=i<=last)
        groups+=f'<div class="part"><div class="part-heading"><h3>{title}</h3></div><div class="chapter-list">{rows}</div></div>'
    body=f'''<main id="main" class="shell"><section class="hero"><div class="hero-copy"><p class="eyebrow">中文图解 · 从器件走向系统</p><h1 class="hero-title">从 ESP32 看懂<br>嵌入式世界。</h1><p class="hero-subtitle">{escape(book['subtitle'])}</p><p class="hero-description">以 ESP32-S3 为主要实验平台，从电路与代码出发，理解传感器、连接、并发、功耗与完整项目。先看清原理，再逐步验证。</p><div class="actions"><a class="button primary" href="{base}read/reading-guide/">从导读开始 →</a><a class="button secondary" href="{base}downloads/ESP32-Atlas.epub" download>下载整本 EPUB ↓</a></div><div class="stats"><div class="stat"><strong>{len(book['chapters'])}</strong><span>正文章节</span></div><div class="stat"><strong>24</strong><span>原创图解</span></div><div class="stat"><strong>7</strong><span>示例程序</span></div></div></div><figure class="hero-art"><img src="{base}assets/images/01.png" alt="嵌入式设备的信息流与能量流示意" fetchpriority="high"><figcaption>原创系统示意，非实际接线图。</figcaption></figure></section><section class="section callout"><h2>先明确实验边界</h2><p>示例程序仅做静态审查，未执行工具链编译或实板烧录。请先阅读导读与各章安全提示，不将教学代码用于关键安全控制。</p><a href="{base}read/qa/">查看本版检查记录 →</a></section><section id="chapters" class="section"><div class="section-heading"><p class="eyebrow">CONTENTS / 全书目录</p><h2>顺序建立概念，也可按问题查阅。</h2></div>{groups}</section><section class="section callout"><h2>资料与完整工程</h2><div class="actions"><a class="button secondary" href="{base}read/glossary/">术语与实验记录</a><a class="button secondary" href="{base}read/sources/">参考资料索引</a><a class="button secondary" href="https://github.com/YZYExp/Learn-ESP32/tree/main/examples">示例程序 ↗</a><a class="button secondary" href="https://github.com/YZYExp/Learn-ESP32/archive/refs/heads/main.zip">下载源文件 ↗</a></div></section></main>'''
    (OUT/'index.html').write_text(page('在线阅读',book['subtitle'],body,base,book))
    (OUT/'search-index.json').write_text(json.dumps(search,ensure_ascii=False))
    (OUT/'.nojekyll').write_text('')
    check_links(base)
    print(f'Built {len(docs)} reading pages and homepage; existing EPUB copied without rebuilding.')
if __name__=='__main__':main()
