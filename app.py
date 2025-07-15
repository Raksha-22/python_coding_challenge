from flask import Flask, request, jsonify
import mysql.connector

app=Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(host='localhost',user='root',password='',database='gutenberg_db')

@app.route('/books',methods=['GET'])
def get_books():
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    
    book_ids=request.args.getlist('book_id')
    languages=request.args.getlist('language')
    mime_types=request.args.getlist('mime_type')
    topics=request.args.getlist('topic')
    authors=request.args.getlist('author')
    titles=request.args.getlist('title')
    page=int(request.args.get('page', 1 ))
    limit=25
    offset=(page-1)*limit
    
    where_clauses=[]
    params=[]
    
    if book_ids:
        where_clauses.append("books.id in (%s)"%','.join(['%s']*len(book_ids))) 
        params.extend(book_ids)   
        
    if languages:
        where_clauses.append("books.language in(%s)"% ','.join(['%s']*len(languages)))
        params.extend(languages)
        
    if authors:
       for a in authors:
           where_clauses.append("lower(books.author) like %s")
           params.append(f"%{a.lower()}%")
           
    if titles:
        for t in titles:
            where_clauses.append("lower(books.title) like %s")
            params.append(f"%{t.lower()}%")
            
    if topics:
        topic_clauses=[]
        for topic in topics:
            topic_clauses.append("lower(subjects.subject)like %s")
            params.append(f"%{topic.lower}%")
        where_clauses.append(f"({' or '.join(topic_clauses)})")
    
    if mime_types:
        mime_clauses=[]
        for m in mime_types:
            mime_clauses.append("formats.mime_type like %s")
            params.append(f"%{m}%")
        where_clauses.append(f"({' or '.join(mime_clauses)})")
        
    
    where_sql=" and ".join(where_clauses)
    if where_sql:
        where_sql="where "+where_sql
        
    count_query=f"""
    select count(distinct books.id)as total
    from books
    left join subjects on books.id=subjects.book_id
    left join formats on books.id=formats.book_id
    {where_sql}
    """
    cursor.execute(count_query, params)
    total_books=cursor.fetchone()['total']
    
    main_query=f"""
    select distinct books.id, books.title, books.author,books.language, books.download_count
    from books
    left join subjects on books.id=subjects.book_id
    left join formats on books.id=formats.book_id
    {where_sql}
    order by books.download_count DESC
    limit %s offset %s
    """
    
    cursor.execute(main_query, params+[limit, offset])
    books=cursor.fetchall()
    
    for book in books:
        book_id=book['id']
        cursor.execute("select mime_type,url from formats where book_id=%s",(book_id,))
        book['formats']=cursor.fetchall()
        cursor.execute("select subject from subjects where book_id=%s",(book_id,))
        book['subjects']=[row['subject']for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'total_books':total_books,
        'page':page,
        'books':books  
        })

if __name__=='__main__':
    app.run(debug=True)