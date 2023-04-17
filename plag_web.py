from flask import Flask,request,render_template
from plagiarism import *



app=Flask(__name__)

@app.route('/',methods=["GET","POST"])


def plagiarism_detect():
    similarity_score=False
    if request.method=="POST":
        
        
        user_input=request.form.get('input_text')
        get_text(user_input)
        get_links(url,get_text(user_input),driver)
        get_data()
        
        similarity_score=plag_detector(user_input)
        
    return render_template('index.html',similarity_score=similarity_score)







if __name__=="__main__":
    app.run(debug=True)
