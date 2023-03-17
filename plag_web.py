from flask import Flask,request,render_template
from plagiarism import *

import nltk
nltk.download('punkt')

app=Flask(__name__)

@app.route('/',methods=["GET","POST"])


def plagiarism_detect():
    if request.method=="POST":
        def get_text(user_input):
            token=nltk.sent_tokenize(user_input)
            return token[0]
        
        user_input=request.form.get('input_text')
        get_text(user_input)
        get_links(url,get_text(user_input))
        get_data()
        plag_detector()
        
    return render_template('index.html')







if __name__=="__main__":
    app.run(debug=True)
