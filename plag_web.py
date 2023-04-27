from flask import Flask,request,render_template
from plagiarism import *
from jinja2 import FileSystemLoader, Environment




app=Flask(__name__)

@app.route('/',methods=["GET","POST"])


def plagiarism_detect():
    error=False
    similarity_score = None
    links = []
    list_of_percentages = []
    if request.method=="POST":
        
        
        user_input=request.form.get('input_text')
        input_validation,sentences=get_text(user_input)
        
        if input_validation==True:
            links=get_links(url,sentences,driver)
            data_list,links_scrapped=get_data(links)
            
            similarity_score,list_of_percentages,links=plag_detector(user_input,data_list,links_scrapped)
        else:
            error="Input more text"
            

    return render_template('index.html',similarity_score=similarity_score,list_of_percentages=list_of_percentages,links=links,error=error)







if __name__=="__main__":
    app.run()
