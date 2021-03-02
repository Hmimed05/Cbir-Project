/************Install Requerements ********************/

pip install requirements.txt

/**************Dataset****************************/
place your data set folders or images inside *app/static/dataset* folder

/****************Indexing ************************/
to create the descriptors for each image follow instructions below :

#####This step it require some time (few minutes for each ) ####


python .\app\Descriptors\color\index.py

python .\app\Descriptors\coocurence\index.py

python .\app\Descriptors\shape\index.py

the results are saved in database folder as csv files 

/***************** RUN THE APP ****************************/

cd ./Image Search Engine/app
python app.py


/***************  How it works *****************************/
when you will run the app it will open a window : http://127.0.0.1:5000/

choose fille : once you choose your image you have to wait for the calculations to finish
it may requeire some few minutes

PS: every file you upload will be saved in Queries folder

after that the results will be retreived in the search results area .



That's it thank you
this project is made by students of MBD and SIM :

El Afia Youness
Hmimed Hamza
Nouiri Hafsa
