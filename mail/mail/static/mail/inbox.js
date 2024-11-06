document.addEventListener('DOMContentLoaded', function() {

  // Process form and send email
  document.querySelector('#compose-form').onsubmit = send_email;

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email=null) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  if (email) {
    // Pre fill composition fields for reply
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value =
      (email.subject.substring(0, 4) === 'Re: ') ? email.subject : `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
  } else {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // ... do something else with emails ...
      emails.forEach(email => {
        load_email_box(email);
      });
  });
}

function load_email_box(email) {
  const email_box = document.createElement('div');
  email_box.className = email.read? 'card bg-light' : 'card bg-primary';
  email_box.addEventListener('click', () => view_email(email.id));

  const sender = document.createElement('div');
  sender.innerHTML = email.sender;
  const subject = document.createElement('div');
  subject.innerHTML = email.subject;
  const timestamp = document.createElement('div');
  timestamp.innerHTML = email.timestamp;

  email_box.append(sender, subject, timestamp);
  document.querySelector('#emails-view').append(email_box);
}

function view_email(email_id) {

  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      // ... do something else with email ...
      document.querySelector('#sender').innerHTML = email.sender;
      document.querySelector('#recipients').innerHTML = email.recipients.join(', ');
      document.querySelector('#subject').innerHTML = email.subject;
      document.querySelector('#body').innerHTML = email.body;
      document.querySelector('#timestamp').innerHTML = email.timestamp;
      document.querySelector('#reply').addEventListener('click', () => compose_email(email));

      // archive button
      const user = document.querySelector('#user').innerText;
      const archive = document.querySelector('#archive');
      if (user === email.sender && !(email.recipients.includes(email.sender))) {
        archive.style.display = 'none';
      } else {
        archive.style.display = 'inline';
        if (email.archived) {
          archive.innerHTML = 'Unarchive';
          archive.className = 'btn btn-secondary';
        } else {
          archive.innerHTML = 'Archive';
          archive.className = 'btn btn-primary';
        }
        archive.addEventListener('click', () => {
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: !email.archived
            })
          });
          load_mailbox('inbox');
          location.reload();
        });
      }

      // mark email as read
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      });
  });
} 

function send_email() {

  // Extract values from form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send email
  fetch('/emails', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      if (result.error !== undefined) {
        alert(`Error: ${result['error']}`);
      }
  })
  // Catch any errors and log them to the console
  .catch(error => {
    console.log('Error:', error);
  });
  load_mailbox('sent');
  return false;
}