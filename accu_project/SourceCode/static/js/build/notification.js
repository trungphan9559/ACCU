// ==========================================================
// =================== NOTIFICATION =========================
// ==========================================================
function show_notification(title, body, url){
  if (!("Notification" in window)) {
    alert("This browser does not support desktop notification");
  }

  // Let's check if the user is okay to get some notification
  else if (Notification.permission === "granted") {
      // If it's okay let's create a notification
    var options = {
            body: body,
            icon: "/static/img/brand/favicon.ico",
            dir : "ltr"
        };
    var notification = new Notification(title,options);
  }

  // Otherwise, we need to ask the user for permission
  // Note, Chrome does not implement the permission static property
  // So we have to check for NOT 'denied' instead of 'default'
  else if (Notification.permission !== 'denied') {
    Notification.requestPermission(function (permission) {
    // Whatever the user answers, we make sure we store the information
    if (!('permission' in Notification)) {
        Notification.permission = permission;
    }

    // If the user is okay, let's create a notification
    if (permission === "granted") {
        var options = {
            body: body,
            icon: "/static/img/brand/favicon.ico",
            dir : "ltr"
        };
        var notification = new Notification("ACCU Notification",options);
    }
    });
  }  

  notification.onclick = function(event) {
      event.preventDefault(); // prevent the browser from focusing the Notification's tab
      window.open(url, '_blank');
      
  }
}