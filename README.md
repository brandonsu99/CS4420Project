# CS4420Project
While it is possible to look at the transcript of an audio file, there is no system available for users to easily query other data points related to the audio file that are not the text that is said. Non-speech based audio files like sounds of nature do not have much room for further analysis. There is some opportunity to do analysis of music audio specifically, but there is still a gap present for speech-based audio files. Non-experts in audio analysis should have the same opportunity to parse audio and conduct analysis on additional features of audio in addition to typical metadata of audio files. 

AQL Library
Set up a database and the tables with the AQL class.
Three constructors: 
basic use case: user is planning to work with a database where the table and features are both set up already.
new database use case: database may not exist yet, or it exists, but it is not set up
use default features use case: the user is about to set up a new database and wants to use the default features provided by the AQL library
 

Use the following SQL commands
Create Database, Create Table, Insert, Insert Batch, Select

Features
Default features: sample rate, number of frames, number of channels, bits per sample, encoding
tempo, classification by the model
If the user fails to pass in a list of features, the AQL library will default to the list of features provided by the library. 
Customisable features: The AQL library also allows for a list of feature tuples to be inserted as the parameter as shown in the first constructor in Figure 5. The features are passed in as a list of tuples where the first item in the tuple is the name of the feature and the second item in the tuple is the method that will get the feature using just the filepath of the audio. The only caveat for the tuple is that the method can only take in one parameter - the file path of the audio file from which features must be extracted. This option allows the user to circumvent the use of the default features provided by AQL, or add additional features to the list of default features. If they want to add additional features to the list, they are able to access all the default features, and then add to that list. 


Two ways to use the library

The first way to use the AQL library is as an object in the code. The user can create an AQL object with the appropriate information regarding the database, table and features they want to use. The constructor builds and object with the relevant information, and then the user has access to the AQL queries through the methods in the class that execute the queries. The user can then call the functions in the class and they will execute appropriately. If there is a result from a query, like with a Select query, the method will return the result for the user to save to a variable and use as they need. 
There is another way to interact with AQL which is more interactive and allows the use of the terminal to execute the queries. When the user runs interactive_AQL.py within the library, they will be prompted to input which database to connect with. The library will be able to take in their command and parse it. They can then use the command line in a similar manner to a SQL query parser with the queries available through AQL. They can type SQL-style queries into the command line which will immediately be executed. For Select queries, the results of the query will be displayed in the terminal for the user to view. This is a similar approach to run queries like in other database systems like SQL, NoSQL.

