# ******************************PYTHON LIBRARIES******************************
import os
from uuid import uuid4
from dataclasses import asdict
# ******************************EXTERNAL LIBRARIES****************************
import pandas
from flask import (Blueprint, 
                    render_template,
                    redirect,
                    request,
                    jsonify)
# ******************************OWN LIBRARIES*********************************
from db import dbBooks, dbNotes
from forms import BookForm, BookAddNotes, BookEditInfo
from objects import Book, Note
# ****************************************************************************
blp = Blueprint("kindle", __name__, template_folder="/app/templates", static_folder="/app/static/css")

bookProperties = ["name", "author", "year", "original_language", "description"]
column_names = ["note_type", "position", "outstanding", "note"]


@blp.route("/home")
def home():
    return render_template("home.html", title="Home page")



@blp.route("/books", methods=["GET", "POST"])
def books():
    global column_names, bookProperties
    
    bookList = dbBooks.find({})
    
    if not request.args.get('option'):
        form = BookForm()
    
    elif request.args.get('option') == 'add':
        form = BookForm()
        if form.validate_on_submit():
            newBook = Book(_id = str(uuid4().hex), 
                            name = form.name.data, 
                            author = form.author.data)
            dbBooks.insert_one(asdict(newBook))
            return render_template("books.html", title="Books Page", bookList=bookList, form=form)
    
    elif request.args.get('option') == 'notes':
        form = BookAddNotes()
        bookID = request.args.get('bookID')
        if form.validate_on_submit():
            notesFile = form.notesFile.data
            fileName = notesFile.filename
            notesFile.save(f"{os.getenv('NOTE_FILES_FOLDER')}/{fileName}")
            kindleFile = pandas.read_csv(f"{os.getenv('NOTE_FILES_FOLDER')}/{fileName}", sep=",")
            df = pandas.DataFrame(kindleFile)
            df.columns = column_names
            name = dbBooks.find_one({"_id": bookID})["name"]
            author = dbBooks.find_one({"_id": bookID})["author"]
            notes = [row[3] for index, row in kindleFile.iterrows() if index > 7]
            if dbNotes.find_one({"bookID": bookID}):
                dbNotes.update_one({"bookID": bookID}, {"$set": {"notes": notes}})
            else:
                newNotes = Note(_id = str(uuid4().hex),
                                bookID = bookID,
                                name = name,
                                author = author,
                                notes = notes)
                dbNotes.insert_one(asdict(newNotes))
                
    elif request.args.get('option') == 'details':
        bookID = request.args.get("bookID")
        bookDetails = dbBooks.find_one({"_id": bookID})
        return render_template("books.html", title="Book Page", bookList=bookList, bookDetails=bookDetails)
    
    elif request.args.get('option') == 'edit':
        form = BookEditInfo()
        bookID = request.args.get('bookID')
        if request.method == "POST":
            newInfo = {key: value for key, value in form.data.items() if value is not "" and value is not None and key in bookProperties}
            dbBooks.update_one({"_id": bookID}, {"$set": newInfo})
            return render_template("books.html", title="Book Page", bookList=bookList, form=form)
        return render_template("books.html", title="Book Page", bookList=bookList, form=form)
    
    elif request.args.get('option') == 'delete':
        bookID = request.args.get('bookID')
        dbBooks.delete_one({"_id": bookID})
        dbNotes.delete_one({"bookID": bookID})
        return render_template("books.html", title="Books Page", bookList=bookList)

    return render_template("books.html", title="Books Page", bookList=bookList, form=form)



@blp.route("/notes")
def notes():
    bookID = request.args.get("bookID")
    book = dbBooks.find_one({"_id": bookID})
    notes = dbNotes.find_one({"bookID": bookID})["notes"]
    return render_template("notes.html", title="Title Page", book=book, notes=notes)



@blp.route("/delete")
def deleteDB():
    dbBooks.delete_many({})
    dbNotes.delete_many({})
    return jsonify({"message": "Databases reseted successfully!"})