const readline = require("readline");
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
const fs = require('fs');
const { exit } = require("process");
const filepath = "./data/user_info.json";
const bcrypt = require('bcrypt');
const saltRounds = 10;

const password= '12345';


//Function to request input data
rl.question("What is your new username?  ",function(name){
    const new_user_name= name;
    rl.question("What is your new password?  ", function(pass){
        const new_user_pass = pass;
        console.log("\nYour new user info:");
        console.log("Name: " + new_user_name);
        console.log("Password: " + new_user_pass + "\n");
        rl.question("Would you like to save this user information?  ",function(auth){
            if(auth === 'yes' || auth === 'y'){
                //Encrypt and store selected password
                bcrypt.hash(new_user_pass,saltRounds, async function(err,hash){
                    if(err){
                        console.log(err);
                        exit;
                    }
                    else{
                        const new_user_pass_hash = hash;
                        console.log('Password Hash: ' + hash);
                        const userinfo = {"user": new_user_name, "password":new_user_pass_hash};
                        const userJSON = JSON.stringify(userinfo);
                        fs.writeFile(filepath,userJSON,function(err){
                            if(err){
                                console.log(err);
                                exit()
                            }
                            else{
                                console.log("Data processed and saved in file: " + filepath);
                                exit()
                            }
                        })
                    }
                })
                
            }
            else{
                console.log("Data was not saved!");
                exit()
            }
        })
    })
});
