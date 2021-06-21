const { request, response } = require('express');
const express = require('express');
const fs = require('fs');
const bcrypt = require('bcrypt');

//Data files
const sp_file = './data/sp_data.json'
const irr_data_file = './data/irr_data.json'
const user_database = './data/user_info.json'

const app = express();

app.listen(3000, ()=> console.log('listening at 3000'));
app.use(express.static('./public'));
app.use(express.json({limit: '1mb'}));

//Function to processes incoming sp
app.post('/sp', (request, response) =>
{
    const received_data = request.body;
    resp_data = process_sp(received_data);
    response.json(resp_data);

});

//Function to handle login data
app.post('/login', async(request, response) =>
{
    console.log('Authenticating user')
    try{
        const received_data = request.body;
        const resp_data = await userAuthenticate(received_data)
        console.log(resp_data);
        response.json(resp_data);    
    }
    catch (err){
        console.log('Error occured')
        response.json({status: "failure"});
    }
});

//Function to retrieve irrigation data from database
app.post('/irr', (request, response) =>
{
    const resp_data = JSON.parse(fs.readFileSync(irr_data_file));
    response.json(resp_data);

});

//Function to retrieves user geo location and save it
app.post('/geo', (request, response) =>{
    const received_data = request.body;
    console.log(received_data);
    response.json(received_data);
})

async function userAuthenticate(userData){
    try{
        const password = userData.p;
        const username = userData.u;
        const userdatabase = await JSON.parse(fs.readFileSync(user_database));
        const db_password = userdatabase["password"];
        const db_username = userdatabase["user"];
        if( db_username === username){
            if(await bcrypt.compare(password, db_password)){
                //If the password matches the saved hashed password in user_info.json
                console.log("Correct username and password")
                return {status: "success"};
            }
            else{
                //If the password does not match the saved hashed password in user_info.json
                console.log("Wrong password used")
                return {status: "failure"};
            }
        }
        else{
            //If the username given does not exist
            console.log("Wrong Username used")
            return {status: "failure"};
        }
    }catch(err){
        //If one of the functions in the try fail
        console.log('User Authentication failed ' + err) 
        return {status: "failure"};
    } 
}

//Function to save the received sp data in the sp_data.json file
function process_sp(data)
{
    const setpoint = data.val;
    const json = {"sp" : setpoint};
    const json_mod = JSON.stringify(json)
    fs.writeFile(sp_file, json_mod, function(err){
        if(err){
            console.log(err);
        }
        else
        {
            console.log("The setpoint was saved");
        }
    });  
    return {status: "success"};

}