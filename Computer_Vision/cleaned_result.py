import Computer_Vision.roboflow_get as roboflow_get

clean_results=""
clas= []
colors=[]
name= None

def clean_magiccolor(image_path,workflow):
    colors=[]
    Number=False
    raw= roboflow_get.roboflow_get(image_path,workflow)
    preds= raw[0]["predictions"]["predictions"]
    cname= raw[0]["open_ai"]

    for i, pred in enumerate(preds):
        clas = pred["class"]
        if clas in ["Red", "White", "Black", "Blue","Green"]:
            colors.append(clas)
        if clas == "Number":
            Number=True
        if clas == "1-Name":
            name=cname[i]["output"]
        
    colors= list(set(colors)) #create unique values in the list

    if len(colors)==0:
        if Number:
            color="Colorless"
        else:
            color="Unknown"
    
    elif len(colors)==1:
        color=colors[0]
    
    elif len(colors)>1:
        color="Multicolor"

    else:
        color="Unknown"

    clean_results= name, color, colors
    return clean_results



