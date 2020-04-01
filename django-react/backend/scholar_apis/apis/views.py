#from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Author, Article
from .serializers import AuthorSerializer, ArticleSerializer
from django.db import connection

#views for fetching authors
@api_view(('GET',))
def AllAuthors(req):
    print(type(req))
    authors = Author.objects.raw('SELECT * FROM Authors')
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

@api_view(('GET',))
def AuthorsById(req, ID):
    author = Author.objects.raw('SELECT * FROM Authors WHERE id = %s', [ID])
    serializer = AuthorSerializer(author, many=True)
    return Response(serializer.data)

@api_view(('GET',))
def AuthorsByName(req, name):
    name = name.replace('+', ' ').lower()
    authors = Author.objects.raw('SELECT * FROM Authors WHERE LOWER(name) = %s', [name])
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

@api_view(('GET',))
def AuthorsByNameAffiliation(req, name, affiliation):
    name = name.replace('+', ' ').lower()
    affiliation = affiliation.replace('+', ' ').lower()
    author = Author.objects.raw('SELECT * FROM Authors WHERE LOWER(name) = %s AND LOWER(affiliation) = %s', [name, affiliation])
    serializer = AuthorSerializer(author, many=True)
    return Response(serializer.data)

# views for fetching articles
@api_view(('GET',))
def AllArticles(req):
    articles = Article.objects.raw('SELECT * FROM Articles')
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(('GET',))
def ArticlesById(req, ID):
    articles = Article.objects.raw('SELECT * FROM Articles WHERE id = %s', [ID])
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(('GET',))
def ArticlesByName(req, name):
    name = name.replace('+', ' ').lower()
    articles = Article.objects.raw('SELECT * FROM Articles WHERE LOWER(name) = %s', [name])
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(('GET',))
def ArticlesByNameAffiliation(req, name, affiliation):
    name = name.replace('+', ' ').lower()
    affiliation = affiliation.replace('+', ' ').lower()
    articles = Article.objects.raw('SELECT * FROM Articles WHERE LOWER(name) = %s AND LOWER(affiliation) = %s', [name, affiliation])
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(('GET',))
def ArticlesByJournal(req, journal):
    journal = journal.replace('+', ' ').lower()
    print('journal: ' + str(journal))
    articles = Article.objects.raw('SELECT * FROM Articles WHERE LOWER(journal) = %s', [journal])
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

#create author, article
@api_view(('POST',))
def AddAuthor(req):
    serializer = AuthorSerializer(data=req.data)
    #print(str(req.getParameter("name")))
    if(serializer.is_valid()):
        with connection.cursor() as cursor:
            print(type(serializer.data))
            name = serializer.data['name']
            affiliation = serializer.data['affiliation']
            name = name.replace('+', ' ')
            affiliation = affiliation.replace('+', ' ')
            cursor.exeute("INSERT INTO AUTHORS(name, affiliation) VALUES (%s, %s )", [name, affiliation])
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def create_author_article(cereal):
    author_fields = ['affiliation', 'pub_title', 'pub_year', 'pub_url', 'citations', 'citedby', 'journal','pub_author']
    sql = 'INSERT INTO ARTICLES(name'
    form = " VALUES (%s"
    values = [cereal['name'].replace("+", ' ')]
    for field in author_fields:
        if(field in cereal):
            values.append(cereal[field].replace('+', ' '))
            sql += ', ' + field
            form += ', ' + '%s'
    sql += ')'
    form += ')'
    result = sql + form
    return result, values;

@api_view(('POST',))
def AddArticle(req):
    serializer = ArticleSerializer(data=req.data)
    #print(str(req.getParameter("name")))
    if(serializer.is_valid()):
        with connection.cursor() as cursor:
            print("SUCCESS!")
            sql, values = create_author_article(serializer.data)
            print(sql)
            print(values)
            cursor.execute(sql, values)
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AllAuthors(generics.ListCreateAPIView):
#     authors = Author.objects.raw('SELECT id, name, affiliation FROM Authors')
#     serializer_class = AuthorSerializer
#
#
# class AuthorById(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Author.objects.all()
#     #print("result: " + str(queryset))
#     serializer_class = AuthorSerializer
