from flask_assets import Bundle

bundles = {
    
    'base_css': Bundle(
        'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css',
        'https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css',
        'css/base.css',
        'css/sidebar.css',
        filters='cssmin',
        output='gen/base.css'
    ),

    'auth_css': Bundle(
        'https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css',
        'css/auth.css',
        'css/base.css',
        filters='cssmin',
        output='gen/auth.css'
    ),

    'auth_js': Bundle(
        'js/auth.js',
        'js/forgot.js',
        filters='jsmin',
        output='gen/auth.js'
    ),
    
    'chat_css': Bundle(
        'css/chat.scss',        
        filters='libsass', 
        output='gen/sass.css'
    ),

    'chat_js': Bundle(
        'js/chat.js',
        filters='jsmin',
        output='gen/chat.js',
     ),

    'img_chat': Bundle(
        'img/imagen_chat.png',
        output='gen/imagen_chat.png'
    ),
    
    'settings_css': Bundle(
        'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css',
        'css/settings.css',
        filters='cssmin',
        output='gen/settings.css'
    ),
    
    'error_css': Bundle(
        'css/error_pages.scss',
        filters='libsass',
        output="gen/errors.css"   
    ),

}
