    // --- START FACEBOOK PLUGIN -----

      window.fbMessengerPlugins = window.fbMessengerPlugins || {
        init: function () {
          FB.init({
            appId            : '2122394994692265',
            autoLogAppEvents : true,
            xfbml            : true,
            version          : 'v3.10'
          });
        }, callable: []
      };
      window.fbAsyncInit = window.fbAsyncInit || function () {
        window.fbMessengerPlugins.callable.forEach(function (item) { item(); });
        window.fbMessengerPlugins.init();
      };
      setTimeout(function () {
        (function (d, s, id) {
          var js, fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) { return; }
          js = d.createElement(s);
          js.id = id;
          js.src = "//connect.facebook.net/en_US/sdk.js";
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
      }, 0);

    // --- END FACEBOOK PLUGIN -----

      // Load and initialise Messenger extensions
      (function(d, s, id){
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.com/en_US/messenger.Extensions.js";
        fjs.parentNode.insertBefore(js, fjs);
      }(document, 'script', 'Messenger'));

      // Messenger SDK ready
      window.extAsyncInit = function() {
        console.log('Messenger extensions are ready');
      }

      // Preloader
      function preloader(){
            document.getElementById("loading").style.display = "none";
            document.getElementById("iframe").style.display = "block";
        }//preloader
        window.onload = preloader;