function activate()
{
	$('.img-editable').not('.img-included').hide();
}
	
function deactivate()
{
	$('.img-editable').not('.img-included').show();
}

$(document).ready(function ()
{
	$('.img-editable').click(function ()
	{
		$(this).toggleClass('img-included');
	});
	
	$('#saveChampionlistButton').click(function ()
	{
		$('.img-included').each(function ()
		{
			var $element_id = $(this).attr('id');
			var $hiddenInput = $('<input />').attr('type', 'hidden');
			$hiddenInput.attr('name', 'champion_id');
			$hiddenInput.attr('value', $element_id);
			$('#championlistForm').append($hiddenInput);
		});
		$('#championlistForm').submit();
	});
	
	$('#toggleChampionVisibility').click(function ()
	{
		$(this).toggleClass('active');
		$(this).hasClass('active') ? activate() : deactivate();
	});
});