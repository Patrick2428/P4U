
const inputName = document.getElementById('username');
const pass = document.getElementById('pass');
const form = document.getElementById('login');
const error = document.getElementById('error_msg');

 
//prevent default event 
form.addEventListener('submit', (e) => 
{
  e.preventDefault()
})

//Event handler for submit button -- checks username and password
async function button_event()
{
  const resp = await check_user_password();
  console.log(resp);
  if (resp === 'success')
  {
    console.log('Password and user name correct')
    window.location.href = './home.html'
  }
  else
  {
    error.innerText = "ERROR: username or password is incorrect";
  }
 
}

// Check password
async function check_user_password()
{
     console.log('Submit pressed');
     const p = pass.value;
     const u = inputName.value;
     const head = 'usr'
     const usr_pass = {head, u, p};
     const options = {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(usr_pass)
        }
     const response = await fetch('/login', options);
     const resp_data = await response.json();
     return resp_data.status;

}
