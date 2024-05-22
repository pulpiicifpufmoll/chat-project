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
        'css/scrollbar.css',
        'css/chat.scss',        
        filters='libsass', 
        output='gen/sass.css'
    ),

    'chat_js': Bundle(
        'https://code.jquery.com/jquery-3.7.1.js',
        'https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.9.2/umd/popper.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.concat.min.js',
        'js/chat.js',
        filters='jsmin',
        output='gen/chat.js',
     ),

    'chat_css': Bundle(
        'css/scrollbar.css',
        'css/chat.scss',
        filters='libsass',
        output='gen/sass.css'),

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
    
    'admin_css': Bundle(
        'https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap',
        'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0',
        'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css',
        'css/admin.css'
    ),
    
    'admin_js': Bundle(
        'js/admin.js',
        filters='jsmin',
        output="gen/admin.js" 
    )
}
