import os
import sys
import json
#from mdutils.mdutils import MdUtils

"""
This script allows the automatic documentation of the _Utilities folder in the ScientISST notebooks repository.

Examples are provided at the end of the script.
"""
'''
def globalDocumentationMD (file_name=None, title=None, folder=None):
    """
    Generates the documentation of the Utilities folder in a Markdown file (.MD).

    Parameters
    ----------
    file_name: str
        Name to be given to the .MD file.
    title : str
        Title of the .MD file.
    folder : str
        Directory where the Utilities folder is located.
    
    Returns
    -------
    md_file: 
        Markdown file containing the documentation collected in the folder.
    """
    
    title=title

    mdFile = MdUtils(file_name=file_name,title=title)

    # body of the document
    dir=folder
    l_dir = os.listdir(dir)

    for f_name in l_dir:
        if f_name.endswith('.py'):

            mdFile.new_header(level=1, title= ' ')
            mdFile.new_header(level=2, title=f_name)

            fileObj = open(f_name, 'r')
            data=fileObj.read()
            s=data

            # find global script description
            p='"""'
            i=s.find(p)
            i2_ = s.find('"""', i+3)
            global_description=data[i:i2_]
            txt=global_description[3:]
            mdFile.new_paragraph(txt)


            mdFile.new_paragraph('This script contains the following functions.')
            
            # find functions
            p="def"
            i1 = s.find(p,0)
            i2 = s.find("(", i1+1)
            i3 = s.find(":", i1+1)
            function_name=data[i1:i2]
            function_def=data[i1:i3]
            txt=function_name[3:]
            mdFile.new_header(level=3, title=txt)
            #mdFile.new_paragraph(function_def,bold_italics_code='i')

            if function_name[3:] != '':
                p_='"""'
                p1_='Parameters'
                i1_=s.find(p_, i1+3)
                i2_ = s.find(p_, i1_+3)
                i3_ = s.find(p1_, i1_+3)
                global_description=data[i1_+5:i3_]
                par_ret=data[i3_-4:i2_]
                mdFile.write(global_description[3:])
                mdFile.new_paragraph(function_def,bold_italics_code='i')
                mdFile.new_paragraph(par_ret)

            while i1 != -1 and i3_ != -1:
                i1 = s.find(p, i2+1)
                i2 = s.find("(", i1+1)
                i3 = s.find(":", i2+1)
                function_name=data[i1:i2]
                function_def=data[i1:i3]
                txt=function_name[3:]
                

                if len(txt) != 0: # cope with functions that use """ within the code (yet not for commenting)
                    if function_name[3]!='"':
                        mdFile.new_header(level=3, title=txt)

                if txt != '' and txt != ' ':
                    # finds description of the function
                    p_='"""'
                    p1_='Parameters'
                    i1_=s.find(p_, i2)
                    i2_ = s.find(p_, i1_+3)
                    i3_ = s.find(p1_, i1_+3)
                    global_description=data[i1_:i3_]
                    if len(global_description) != 0 and global_description[3]!='"': # cope with functions that use """ within the code (yet not for commenting)
                        global_description=data[i1_+5:i3_]
                        par_ret=data[i3_-4:i2_]
                        mdFile.write(global_description[3:])
                        mdFile.new_paragraph(function_def,bold_italics_code='i')
                        mdFile.new_paragraph(par_ret)

                i3_ = s.find(p1_, i3_+10)

    mdFile.create_md_file()

    return mdFile
'''
def dirFiles(dir=None):
    """
    Finds notebooks in a directory and collects relevant information from each, to return a comprehensive table of contents and information regarding all notebooks found.
    
    Parameters
    ----------
    dir: string
        Directory path of the repository.
    """

    l_dir = sorted(os.listdir(dir))
    
    for f_name in l_dir:
        if f_name.endswith('.ipynb') and f_name not in ['A002 Science Journal.ipynb']:
            path=dir + f_name
            
            f_name=f_name[:-6]
            print(f_name)

            statbuf = os.stat(path)
            timestamp=statbuf.st_mtime
            datetime_ = datetime.fromtimestamp(timestamp)
            print("datetime =", datetime_)
            f=open(path,"r")
            data = f.read()
            jsonObj = json.loads(data)

            keylist = jsonObj.keys()
            itemslist = jsonObj.items()
            
            for i in range(0,len(jsonObj['cells'])):
                source=str(jsonObj['cells'][i]['source'][0])
                if i==len(jsonObj['cells'])-1:
                    if source.startswith('```'):
                        author=source[17:-3]
                    else:
                        author='Prof. Hugo Silva, Joana Pinto'
                elif i==2:
                    tags=''
                    if source.startswith('```'):
                        mylist = source.split(',')
                        nb_tags=len(mylist)
                        for e in range(0,nb_tags):
                            elem=mylist[e]
                            if elem[3]=='`':
                                elem=elem[4:-3]
                            else:
                                elem=elem[3:-3]
                            tags+=str(elem)+', '
                        print (tags)
                        
            if f_name[0]=='A':
                chapter='A. Signal Acquisition'
            elif f_name[0]=='B':
                chapter='B. Graphical User Interface'
            elif f_name[0]=='C':
                chapter='C. Signal Processing'
            elif f_name[0]=='D':
                chapter='D. Feature Extraction'
            elif f_name[0]=='E':
                chapter='E. Classification'
            elif f_name[0]=='F':
                chapter='F. Applications'

            md_file.write(f_name[0:4] +' | ')
            md_file.write(f_name[4:] +' | ')
            md_file.write(chapter +' | ')
            md_file.write(str(tags[:-1])+'|')
            md_file.write(author +'|')
            md_file.write(str(datetime_)[0:10]+'|'+'\n')
        print('i')

def createMasterTable(file_name=None):
    file_name=file_name
    with open(os.path.join('../../','{}.md'.format(file_name)), mode='w') as md_file:
        md_file.write("# ScientISST Notebooks \n This Table provides an overview to the complete set of notebooks made available in this repository. \n \n These are independent and can be selected independently and organized as most suits the purpose of the course.  \n\n ## Detailed Repository:  \n")
        md_file.write("ID | Name | Chapter | Tags | Authors | Last update \n")
        md_file.write("--- | --- | --- | --- | --- | --- \n")
        dirFiles(dir='../../A.Signal_Acquisition/')
        dirFiles(dir='../../B.Graphical_User_Interface/')
        dirFiles(dir='../../C.Signal_Processing/')
        dirFiles(dir='../../D.Feature_Extraction/')
        dirFiles(dir='../../E.Classification/')
        dirFiles(dir='../../F.Applications/')

def searchRepository(find_=None, author_=None,keyword=None,MasterTable=None):
        f=open(MasterTable,"r")
        #text=f.read()
        lines=f.readlines()
        result=[]
        count=0

        # Strips the newline character
        for line in lines:
            count += 1
            score=0
            if count>7:
                fields = line.split("|")
                #print(len(fields))
                id=fields[0]
                title=fields[1]#
                folder=fields[2]
                keyword=fields[3]
                author=fields[4]

                if find_ != None:
                    i=title.strip().lower().find(find_.lower())
                    if i!=-1:
                        score+=1
                    
                    i=keyword.strip().lower().find(find_.lower())
                    if i!=-1:
                        score+=1
                    if score>0:
                        result.append([id,title,folder])
                        #print(id,title,score)
                
                if author_ != None:
                    i=author.strip().lower().find(author_.lower())
                    if i!=-1:
                        score+=1
                    
                    if score>0:
                        result.append([id,title,folder])
                
        #print(result)
        #print(result.sort(key=elem[1] for elem in result )
        #print(id,title,score)

        notebook='searchResult.ipynb'
        r = open(notebook,"r")
        data = r.read()
        jsonObj = json.loads(data)
        keylist = jsonObj.keys()
        #print(keylist)

        itemslist = jsonObj.items()
        length=len(jsonObj['cells'])
        for i in range(0,length):
            dict_=dict(jsonObj['cells'][i])
            dict_keys=dict_.keys()

            if dict_['cell_type']=='markdown':
                # adiciona cabecalho
                if i == 1:
                    
                    dict_['source'][0]=find_
                    
                if i == 3:
                    #for d in dict_['source']:
                    #    dict_['source'][d]=[]
                    print(len(dict_['source']))
                    ls=len(dict_['source'])
                    lr=len(result)
                    print(lr,ls)
                    j=0
                    for r in result:
                        
                        print(j)
                        if j in range (0,ls):
                            print(j)
                            folder=r[2]
                            title=r[1]
                            ID=r[0]
                            folder=folder[1:-1].replace(" ","_")
                            folder=folder.replace("._",".")
                            print(folder)
                            a=str('(../'+folder+'/'+ID+title+'.ipynb)')
                            a=a.replace('/ ','/')
                            a=a.replace(' .','.')
                            a=a.replace('   ',' ')
                            print(a)
                            dict_['source'][j]='['+str(title)+']'+a+'<br>'
                            
                        elif lr> ls:
                            dict_['source'].append(str(r)+'<br>')
                            
                        j+=1
                    if ls>lr:
                        for s in range(lr,ls):
                            print('apaguei')
                            dict_['source'].remove(dict_['source'][j])
                            print('apaguei')        

        f.seek(0) 
        with open(notebook, 'w') as json_data:
            json.dump(jsonObj, json_data)

searchRepository(find_='signal', MasterTable='../MasterTable.md')
#searchRepository(find_='poincare', MasterTable='../MasterTable.md')
#searchRepository(author_='Joana', MasterTable='../MasterTable.md')

#globalDocumentationMD(file_name='README', tile='Global Documentation - ScientISST Utilities', folder='.')

#createMasterTable(file_name="MasterTable")