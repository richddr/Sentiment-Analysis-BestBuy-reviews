__author__ = 'Richard Garcia || Ricardo Batista'
from pprint import pprint
from Tkinter import *
import requests
import time
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

tokenizer = RegexpTokenizer(r'\w+')
stop = stopwords.words('english')
pos_sent = open('positive.txt').read()
neg_sent = open('negative.txt').read()
positive_words = pos_sent.split('\n')
negative_words = neg_sent.split('\n')

apiKey = 'b5pnf35czhffjtn63d6t2hvp'
green = True
no_tiene = "API no retorna reviews para ese producto"

def update_the_label():
    entrada = e1.get()
    sku = entrada

    #Detalles del producto
    p = requests.get("http://api.remix.bestbuy.com/v1/products(sku=" +sku+")?show=name,description,shortDescription,longDescription,height,width,depth,weight&format=json&apiKey="+apiKey)
    producto = p.json()['products'][0]

    #Detalles de los reviews del producto
    r = requests.get(
        "http://api.remix.bestbuy.com/v1/reviews(sku=" + sku + ")?format=json&apiKey=" + apiKey + "&show=id,sku,title,comment,rating,reviewer.name&pageSize=100")
    json_tmp = r.json()
    total_pages = int(json_tmp['totalPages'])
    print("TOTAL_PAGES: " + str(total_pages))
    positive_counts = 0
    negative_counts = 0
    product_rating = 0
    reviews_count = 0
    #(total_pages > 100)? 100 : total_pages
    total_pages = 100 if (total_pages > 100) else total_pages
    if int(json_tmp['total']) > 0 and int(json_tmp['totalPages']) > 0:
        for i in range(1, 4):
            print("SE HACE LLAMADA")
            p = requests.get(
            "http://api.remix.bestbuy.com/v1/reviews(sku=" + sku + ")?format=json&apiKey=" + apiKey + "&show=id,sku,title,comment,rating,reviewer.name&pageSize=100&page="+str(i))
            json = p.json()
            print("FROM: " + str(json['from']))
            print("TO: " + str(json['to']))
            print("TOTAL: " + str(json['total']))
            print("CURRENT PAGE: " + str(json['currentPage']))
            for review in json['reviews']:
                rating = review['rating']
                full_review = review['title'] + ' ' + review['comment']
                print('REVIEW: ' + full_review)
                reviews_count += 1
                product_rating += rating
                positive_counter = 0
                negative_counter = 0
                veredicto_producto = ''
                tokenized_review_words = []
                #limpiamos las palabras, tokenizando, quitando signos de puntuacion, quitando stopwords
                for word in tokenizer.tokenize(full_review.lower()):
                    if word not in stop:
                        tokenized_review_words.append(word)
                #chequeamos las palabras positivas y negativas
                for word in tokenized_review_words:
                    if word in positive_words:
                        positive_counter += 1
                    if word in negative_words:
                        negative_counter += 1
                positive_counts += (positive_counter/float(len(tokenized_review_words)))
                negative_counts += (negative_counter/float(len(tokenized_review_words)))
            #time.sleep(0.25)
        print("Total Positivo: " + str(positive_counts))
        print("Total Negativo: " + str(negative_counts))
        print("Average Rating: " + str(product_rating/reviews_count))
        if positive_counts > negative_counts:
            green = True
            veredicto_producto = "Tiene un sentiment positivo, a la gente le gusta!"
            print("Este producto: "+producto['name']+" tiene un sentiment positivo, a la gente le gusta!")
        else:
            green = False
            veredicto_producto = "Tiene un sentiment negativo, no gusta!!!"
            print("Este producto: "+producto['name']+"  tiene un sentiment negativo, no gusta!!!")
        resultadoPositivo = positive_counts
        resultadoNegativo = negative_counts

        resultado1.configure(text="Porcentaje Positivo: {0}".format(resultadoPositivo))
        resultado2.configure(text="Porcentaje Negativo: {0}".format(resultadoNegativo))
        nombre.configure(text="Nombre: {0}".format(producto['name']))
        averaje.configure(text="Averaje: {0}".format(str(product_rating/reviews_count)))
        veredicto.configure(text="Veredicto: {0}".format(veredicto_producto))
    else:
        resultado1.configure(text="Porcentaje Positivo: {0}".format(no_tiene))
        resultado2.configure(text="Porcentaje Negativo: {0}".format(no_tiene))
        nombre.configure(text="Nombre: {0}".format(producto['name']))
        averaje.configure(text="Averaje: {0}".format(no_tiene))
        veredicto.configure(text="Veredicto: {0}".format(no_tiene))

#Esto se obtiene del producto que se desee evaluar, se debe insertar por la GUI
sku = '8240103'


def product_sentiment():
    #Detalles del producto
    p = requests.get("http://api.remix.bestbuy.com/v1/products(sku=" +sku+")?show=name,description,shortDescription,longDescription,height,width,depth,weight&format=json&apiKey="+apiKey)
    producto = p.json()['products'][0]

    #Detalles de los reviews del producto
    r = requests.get(
        "http://api.remix.bestbuy.com/v1/reviews(sku=" + sku + ")?format=json&apiKey=" + apiKey + "&show=id,sku,title,comment,rating,reviewer.name&pageSize=100")
    json_tmp = r.json()
    total_pages = int(json_tmp['totalPages'])
    print("TOTAL_PAGES: " + str(total_pages))
    positive_counts = 0
    negative_counts = 0
    product_rating = 0
    reviews_count = 0
    #(total_pages > 100)? 100 : total_pages
    total_pages = 100 if (total_pages > 100) else total_pages

    for i in range(1, 4):
        print("SE HACE LLAMADA")
        p = requests.get(
        "http://api.remix.bestbuy.com/v1/reviews(sku=" + sku + ")?format=json&apiKey=" + apiKey + "&show=id,sku,title,comment,rating,reviewer.name&pageSize=100&page="+str(i))
        json = p.json()
        print("FROM: " + str(json['from']))
        print("TO: " + str(json['to']))
        print("TOTAL: " + str(json['total']))
        print("CURRENT PAGE: " + str(json['currentPage']))
        for review in json['reviews']:
            rating = review['rating']
            full_review = review['title'] + ' ' + review['comment']
            #print('REVIEW: ' + full_review)
            reviews_count += 1
            #print(reviews_count)
            product_rating += rating
            positive_counter = 0
            negative_counter = 0
            tokenized_review_words = []
            #limpiamos las palabras, tokenizando, quitando signos de puntuacion, quitando stopwords
            for word in tokenizer.tokenize(full_review.lower()):
                if word not in stop:
                    tokenized_review_words.append(word)
            #print(tokenized_review_words)
            #chequeamos las palabras positivas y negativas
            for word in tokenized_review_words:
                if word in positive_words:
                    positive_counter += 1
                if word in negative_words:
                    negative_counter += 1
            positive_counts += (positive_counter/float(len(tokenized_review_words)))
            negative_counts += (negative_counter/float(len(tokenized_review_words)))
        #time.sleep(0.25)
    print("Total Positivo: " + str(positive_counts))
    print("Total Negativo: " + str(negative_counts))
    print("Average Rating: " + str(product_rating/reviews_count))
    if positive_counts > negative_counts:
        print("Este producto: "+producto['name']+" tiene un sentiment positivo, a la gente le gusta!")
    else:
        print("Este producto: "+producto['name']+"  tiene un sentiment negativo, no gusta!!!")

root = Tk()
l1 = Label(root, text="Ingrese el codigo del libro:")
l1.pack()

e1 = Entry(root)
e1.pack()

b = Button(root, text="Analizar", command=update_the_label)
b.pack()

nombre = Label(root, text=" ")
nombre.pack()

nombre = Label(root, text=" ")
nombre.pack()

averaje = Label(root, text=" ")
averaje.pack()

resultado1 = Label(root, text=" ")
resultado1.pack()

resultado2 = Label(root, text=" ")
resultado2.pack()

veredicto = Label(root, text=" ", fg="red" if not green else "green")
veredicto.pack()

root.mainloop()
#product_sentiment()