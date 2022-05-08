var socket = io();

socket.on('connect', function(){
  socket.emit('connected', user);
});

socket.on('sending_file', function(filename, filedata, sender){
  if(window.confirm("A file named '"+filename+"' is coming from '"+sender+"'.\nDo you wish to download it?")){
    var blob = new Blob([filedata])
    var link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    socket.emit('confirmation', filename, sender);
    socket.emit('print', filename + " received!");
  }
})

socket.on('alert', function(text){
  window.alert(text)
})
