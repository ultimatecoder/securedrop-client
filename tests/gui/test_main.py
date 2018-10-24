"""
Check the core Window UI class works as expected.
"""
from PyQt5.QtWidgets import QApplication, QVBoxLayout
from PyQt5.QtCore import QTimer
from securedrop_client.gui.main import Window
from securedrop_client.gui.widgets import LoginDialog
from securedrop_client.resources import load_icon


app = QApplication([])


def test_init(mocker):
    """
    Ensure the Window instance is setup in the expected manner.
    """
    mock_li = mocker.MagicMock(return_value=load_icon('icon.png'))
    mock_lo = mocker.MagicMock(return_value=QVBoxLayout())
    mock_lo().addWidget = mocker.MagicMock()
    _ = mocker.patch('securedrop_client.gui.main.load_icon', mock_li)
    mock_tb = mocker.patch('securedrop_client.gui.main.ToolBar')
    mock_mv = mocker.patch('securedrop_client.gui.main.MainView')
    _ = mocker.patch('securedrop_client.gui.main.QVBoxLayout', mock_lo)
    mock_qmw = mocker.patch('securedrop_client.gui.main.QMainWindow')

    w = Window()
    mock_li.assert_called_once_with(w.icon)
    mock_tb.assert_called_once_with(w.widget)
    mock_mv.assert_called_once_with(w.widget)
    assert mock_lo().addWidget.call_count == 2


def test_setup(mocker):
    """
    Ensure the passed in controller is referenced and the various views are
    instantiated as expected.
    """
    w = Window()
    mock_controller = mocker.MagicMock()
    w.setup(mock_controller)
    assert w.controller == mock_controller


def test_autosize_window(mocker):
    """
    Check the autosizing fits to the full screen size.
    """
    w = Window()
    w.resize = mocker.MagicMock()
    mock_screen = mocker.MagicMock()
    mock_screen.width.return_value = 1024
    mock_screen.height.return_value = 768
    mock_sg = mocker.MagicMock()
    mock_sg.screenGeometry.return_value = mock_screen
    mock_qdw = mocker.MagicMock(return_value=mock_sg)
    _ = mocker.patch('securedrop_client.gui.main.QDesktopWidget', mock_qdw)
    w.autosize_window()
    w.resize.assert_called_once_with(1024, 768)


def test_show_login(mocker):
    """
    The login dialog is displayed with a clean state.
    """
    mock_controller = mocker.MagicMock()
    w = Window()
    w.setup(mock_controller)
    mock_ld = mocker.patch('securedrop_client.gui.main.LoginDialog')
    w.show_login()
    mock_ld.assert_called_once_with(w)
    w.login_dialog.reset.assert_called_once_with()
    w.login_dialog.exec.assert_called_once_with()


def test_show_login_error(mocker):
    """
    Ensures that an error message is displayed in the login dialog.
    """
    mock_controller = mocker.MagicMock()
    w = Window()
    w.setup(mock_controller)
    w.login_dialog = mocker.MagicMock()
    w.show_login_error('boom')
    w.login_dialog.error.assert_called_once_with('boom')


def test_hide_login(mocker):
    """
    Ensure the login dialog is closed and hidden.
    """
    mock_controller = mocker.MagicMock()
    w = Window()
    w.setup(mock_controller)
    ld = mocker.MagicMock()
    w.login_dialog = ld
    w.hide_login()
    ld.accept.assert_called_once_with()
    assert w.login_dialog is None


def test_show_sources(mocker):
    """
    Ensure the sources list is passed to the source list widget to be updated.
    """
    w = Window()
    w.main_view = mocker.MagicMock()
    w.show_sources([1, 2, 3])
    w.main_view.source_list.update.assert_called_once_with([1, 2, 3])


def test_show_sync(mocker):
    """
    If there's a value display the result of its "humanize" method.
    """
    w = Window()
    w.main_view = mocker.MagicMock()
    updated_on = mocker.MagicMock()
    w.show_sync(updated_on)
    w.main_view.status.setText.assert_called_once_with('Last Sync: ' +
                                                       updated_on.humanize())


def test_show_sync_no_sync(mocker):
    """
    If there's no value to display, default to a "waiting" message.
    """
    w = Window()
    w.main_view = mocker.MagicMock()
    w.show_sync(None)
    w.main_view.status.setText.\
        assert_called_once_with('Waiting to Synchronize')


def test_set_logged_in_as(mocker):
    """
    Given a username, the toolbar is appropriately called to update.
    """
    w = Window()
    w.tool_bar = mocker.MagicMock()
    w.set_logged_in_as('test')
    w.tool_bar.set_logged_in_as.assert_called_once_with('test')


def test_logout(mocker):
    """
    Ensure the toolbar updates to the logged out state.
    """
    w = Window()
    w.tool_bar = mocker.MagicMock()
    w.logout()
    w.tool_bar.set_logged_out.assert_called_once_with()


def test_on_source_changed(mocker):
    """
    Ensure the event handler for when a source is changed calls the
    show_conversation_for method with the expected source object.
    """
    w = Window()
    w.main_view = mocker.MagicMock()
    mock_si = w.main_view.source_list.currentItem()
    mock_sw = w.main_view.source_list.itemWidget()
    w.show_conversation_for = mocker.MagicMock()
    w.on_source_changed()
    w.show_conversation_for.assert_called_once_with(mock_sw.source)


def test_conversation_for(mocker):
    """
    TODO: Finish this once we have data. Currently checks only the GUI layer
    is called in the expected manner with dummy data.
    """
    w = Window()
    w.main_view = mocker.MagicMock()
    mock_conview = mocker.MagicMock()
    mock_source = mocker.MagicMock()
    mock_source.journalistic_designation = 'Testy McTestface'
    _ = mocker.patch('securedrop_client.gui.main.ConversationView',
                     mock_conview)
    w.show_conversation_for(mock_source)
    conv = mock_conview()
    assert conv.add_message.call_count > 0
    assert conv.add_reply.call_count > 0
