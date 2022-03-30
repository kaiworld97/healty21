function editListener(id) {
    const self = $(`.comment_edit_${id}`);
    let form = self.parents('form');
    let textarea = form.find('textarea');

    if (self.val() == '수정') {
        textarea.attr('readonly', false);
        self.val('수정완료');
    } else {
        self.val('수정');
        textarea.attr('readonly', true);
        form.submit();
    }
}
