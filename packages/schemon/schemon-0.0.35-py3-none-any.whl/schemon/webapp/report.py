import nicegui.elements.button
from nicegui import ui, run
from schemon.model import ApprovalResultEnum
from schemon import dao
from schemon.common import TempConstant
from schemon.validate import approve


def get_current_user():
    """TODO: get current user id"""
    return TempConstant.APPROVER_ID


result_text = {
    ApprovalResultEnum.approved: "Approved",
    ApprovalResultEnum.rejected: "Rejected",
}

approval_button_group = []
status_label: nicegui.elements.label.Label = None


def do_approve(pr_id: str, repo_id: str, approval_result: ApprovalResultEnum) -> callable:
    async def func():
        global status_label
        [b.set_enabled(False) for b in approval_button_group]
        text = result_text.get(approval_result)
        ret = await run.io_bound(approve, pr_id, repo_id, approval_result)
        status_label.set_text(text)
        notify_type = 'positive' if ret.success else 'warning'
        ui.notify(ret.message, multi_line=True, classes='multi-line-notification', type=notify_type)
        [b.set_enabled(True) for b in approval_button_group]

    return func


def report(pr_id: str, repo_id: str):
    ui.html('<style>.multi-line-notification { white-space: pre-line; }</style>')
    ui.page.title = f"Validation Report for PR #{pr_id}"
    found_report = True
    result = dao.get_validation_result(pr_id, repo_id)
    result_status = ""
    if not result:
        report_content = f"## Report for PR #{pr_id} Not Found"
        found_report = False
    else:
        report_content = result.content
        approval_result = dao.get_validation_result_approval(result.result_id, get_current_user())
        result_status = result_text.get(approval_result, "Pending")

    global approval_button_group, status_label
    with ui.card().classes('w-2/3 mx-auto mt-20'):
        if found_report:
            with ui.row().classes('justify-center mt-4'):
                bt1 = ui.button('Approve').classes('mx-2')
                bt2 = ui.button('Reject').classes('mx-2')
                approval_button_group.extend([bt1, bt2])
                status_label = ui.label(result_status).classes('text-lg text-center ml-4')
                bt1.on_click(do_approve(pr_id, repo_id, ApprovalResultEnum.approved))
                bt2.on_click(do_approve(pr_id, repo_id, ApprovalResultEnum.rejected))
                # ui.label(f"result_id #{result.result_id}").classes('text-lg text-center')
        ui.markdown(report_content).classes('text-lg p-4')
