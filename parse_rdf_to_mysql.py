from rdflib import Graph, Namespace,RDF
from rdflib.namespace import DCTERMS
import os
import mysql.connector

PGTERMS= Namespace('http://www.gutenberg.org/2009/pgterms/')

conn=mysql.connector.connect(host='localhost',
                             user='root', password='',database='gutenberg_db')
cursor=conn.cursor()

cursor.execute("""create table if not exists books(
    id int primary key,
    title varchar(255),
    author varchar(255),
    language varchar(10),
    download_count int
    );"""
)

cursor.execute(""" create table if not exists formats(
    id int auto_increment primary key,
    book_id int,
    mime_type varchar(100),
    url text,
    foreign key(book_id) references books(id)
    );"""
)

cursor.execute("""create table if not exists subjects(
    id int auto_increment primary key,
    book_id int,
    subject text,
    foreign key(book_id) references books(id)
    );"""
)

rdf_dir='rdf-files/cache/epub'

for root, _, files in os.walk(rdf_dir):
    for file in files:
        if file.endswith('.rdf'):
            book_id=int(file.replace('pg','').replace('.rdf',''))
            g=Graph()
            g.parse(os.path.join(root,file))
            
            ebook_subject=None
            for s in g.subjects(RDF.type,PGTERMS.ebook):
                    ebook_subject=s
                    break
            if not ebook_subject:
                continue
            
            
                    
            title=g.value(ebook_subject,DCTERMS.title)
            
            download_count=g.value(ebook_subject,PGTERMS.downlods)
            
            author=None
            creator_node=g.value(ebook_subject,DCTERMS.creator)
            if creator_node:
                author=g.value(creator_node,PGTERMS.name)
                
            language=None
            lang_node=g.value(ebook_subject,DCTERMS.language)
            if lang_node:
                language=g.value(lang_node,RDF.value)     
                       
            cursor.execute("""insert ignore into books(id,title,author,language,download_count) values(%s,%s, %s, %s, %s)""",(book_id,str(title)if title else None,str(author) if author else None,str(language) if language else None,int(download_count or 0)))
            
            for s in g.objects(ebook_subject,DCTERMS.subject):
                subject_text=g.value(s,RDF.value)
                if subject_text:
                    cursor.execute("""insert into subjects(book_id,subject) values(%s,%s)""",(book_id,str(subject_text)))
                
            for fmt in g.objects(ebook_subject,DCTERMS.hasFormat):
                fmt_url=str(fmt)
                if 'http' in fmt_url:
                    mime=fmt_url.split('.')[-1][:50]
                    cursor.execute("insert into formats(book_id,mime_type,url)values(%s,%s,%s)",(book_id,mime,fmt_url))
            

conn.commit()
cursor.close()
conn.close()    
print("Success");        