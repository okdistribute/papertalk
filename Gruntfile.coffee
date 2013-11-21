module.exports = (grunt) ->
  grunt.initConfig

    coffee:
      compile:
        expand: true           # enable dynamic expansion
        cwd: 'papertalk/static/coffee'      # source dir for coffee files
        src: '**/*.coffee'     # traverse *.coffee files relative to cwd
        dest: 'papertalk/static/js'      # destination for compiled js files
        ext: '.js'             # file extension for compiled files


    watch:
      scripts:
        files: ['papertalk/static/coffee/**/*.coffee']
        tasks: ['coffee']
        options:
          spawn: false


  grunt.loadNpmTasks "grunt-contrib-coffee"
  grunt.loadNpmTasks "grunt-contrib-watch"

  grunt.registerTask "default", ["coffee"]
  grunt.registerTask "build", ["coffee"]
  grunt.registerTask "deploy", ["copy", "build", "clean"]
  grunt.registerTask 'heroku:production', 'build'
  grunt.registerTask 'heroku:development', 'build'
