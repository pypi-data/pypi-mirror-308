""" Testing Input Package Init Module Methods.
"""
from pathlib import Path
from unittest.mock import Mock

import pytest
from changelist_data.storage import ChangelistDataStorage, StorageType, storage_type
from changelist_data.xml import workspace
from changelist_data.xml.changelists import new_tree

from changelist_sort.input import validate_input
from changelist_sort.sorting.sort_mode import SortMode
from test import data_provider
from test.data_provider import get_simple_changelist_xml, get_multi_changelist_xml
from test.test_init import wrap_tree_in_storage


def create_storage(tree = new_tree()) -> ChangelistDataStorage:
    return wrap_tree_in_storage(tree)

@pytest.fixture()
def simple_storage():
    return wrap_tree_in_storage(workspace.read_xml(get_simple_changelist_xml()))

@pytest.fixture()
def multi_storage():
    return wrap_tree_in_storage(workspace.read_xml(get_multi_changelist_xml()))


def test_validate_input_no_args_ws_file_does_not_exist_raises_exit(monkeypatch):
    test_input = []
    monkeypatch.setattr(Path, 'exists', lambda _: False)
    #
    result = validate_input(test_input)
    #
    assert len(result.storage.get_changelists()) == 0
    assert result.storage.storage_type == StorageType.CHANGELISTS
    assert result.storage.update_path == storage_type.get_default_path(StorageType.CHANGELISTS)
    #
    assert result.sort_mode == SortMode.MODULE
    assert not result.remove_empty


def test_validate_input_no_args_ws_file_is_empty_raises_exit(monkeypatch):
    test_input = []
    monkeypatch.setattr(Path, 'exists', lambda _: True)
    monkeypatch.setattr(Path, 'read_text', lambda _: '')
    result = validate_input(test_input)
    assert len(result.storage.get_changelists()) == 0


def test_validate_input_no_args_ws_file_has_no_cl_():
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda p: p.name == '.idea/workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
    assert len(result.storage.get_changelists()) == 0


def test_validate_input_no_args_ws_file_simple_cl_():
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda p: True)
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_cl_simple_xml())
        result = validate_input(test_input)
    assert len(result.storage.get_changelists()) == 1


def test_validate_input_no_args_ws_file_multi_cl_(multi_storage):
    test_input = []
    def storage_expects(storage_type, path):
        if storage_type is not None:
            exit("Provided Storage Type was None")
        if path is not None:
            exit("Provided Path was None")
        return multi_storage
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda p: True)
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_cl_multi_xml())
        result = validate_input(test_input)
        assert len(result.storage.get_changelists()) == 2



def test_validate_input_ws_path_arg_is_empty_raises_exit():
    test_input = ['--workspace', '']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_ws_path_arg_is_missing_raises_exit():
    test_input = ['--workspace']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_ws_path_arg_does_not_exist_raises_exit():
    test_input = ['--workspace', '/file.xml']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_developer_sort():
    test_input = ['-d']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda p: p.name == '.idea/workspace.xml')
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
        #
        assert result.sort_mode == SortMode.DEVELOPER
        #
        assert len(result.storage.get_changelists()) == 0


def test_validate_input_sourceset_sort():
    test_input = ['-s']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda p: p.name == '.idea/workspace.xml')
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
        #
        assert result.sort_mode == SortMode.SOURCESET
        #
        assert len(result.storage.get_changelists()) == 0


def test_validate_input_remove_empty():
    test_input = ['-r']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda p: p.name == '.idea/workspace.xml')
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
        #
        assert result.sort_mode == SortMode.MODULE
        assert result.remove_empty
        assert len(result.storage.get_changelists()) == 0
