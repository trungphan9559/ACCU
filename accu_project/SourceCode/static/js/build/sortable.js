function disable_sortable_item($item){
  $item.removeClass('sorting-initialize')
  disable_element($item)
};

function enable_sortable_item($item){
  $item.addClass('sorting-initialize')
  enable_element($item)
};