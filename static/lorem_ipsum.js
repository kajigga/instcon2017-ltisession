$(document).ready(function(){
 $('button').click(function(){
 $('#wanted_submit_btn').show();
 });

 $('#kitten_btn').click(function(){
 $('#wanted_type').val('img');
 $('#kitten_fields').show();
 $('#lorem_fields, #iframe_fields').hide();
 });
 $('#kitten_fields').change(function(){
 // height/width
 var img_src = 'https://placekitten.com/g/'+ $('#height').val() +'/'+ $('#width').val() ;
 $('#kitten_preview')
 .attr('height', $('#height').val() + 'px')
 .attr('width', $('#width').val() + 'px')
 .attr('src', img_src)
 });
 $('#lorem_btn').click(function(){
 $('#wanted_type').val('oembed');
 $('#lorem_fields').show();
 $('#kitten_fields, #iframe_fields').hide();
 });
 $('#embed_iframe_btn').click(function(){
 $('#wanted_type').val('iframe');
 $('#iframe_fields').show();
 $('#lorem_fields, #kitten_fields').hide();
 });
 $('#random_btn').click(function(){
 $('#wanted_type').val('iframe');
 $('#random_fields').show();
 $('#iframe_fields, lorem_fields, #kitten_fields').hide();
 });
 $('#iframe_fields').change(function(){
 var height = $('#iframe_height').val() == '' ? $('#iframe_preview').attr('height') : $('#iframe_height').val();
 var width = $('#iframe_width').val() == '' ? $('#iframe_preview').attr('width') : $('#iframe_width').val();
 $('#iframe_preview')
 .attr('src', $('#iframe_url').val())
 .attr('height', height + 'px')
 .attr('width', width + 'px');
 });
});