from pathlib import Path

from src.docx_merge.index import merge_docx


def test_merge_docx():
    source_path = "tests/fixtures/template.docx"
    content_path = "tests/fixtures/table.docx"
    output_path = "tests/fixtures/output.docx"
    pattern = "{{table}}"
    assert Path(source_path).exists()
    assert Path(content_path).exists()
    assert not Path(output_path).exists()

    # Merge the DOCX files
    output_stream = merge_docx(
        source_path=source_path,
        content_path=content_path,
        output_path=output_path,
        pattern=pattern,
        insert_start=True,
        insert_end=True,
    )
    assert output_stream is not None
    assert Path(output_path).exists()
    # Clean up the output file after the test
    Path(output_path).unlink(missing_ok=True)
    assert not Path(output_path).exists()


def test_merge_docx_no_source_paths():
    pattern = "{{table}}"
    try:
        merge_docx(source_path="", content_path="", pattern=pattern)
    except ValueError as e:
        assert str(e) == "Source file path cannot be empty."
    else:
        raise AssertionError("Expected ValueError not raised.")


def test_merge_docx_no_content_paths():
    source_path = "tests/fixtures/template.docx"
    pattern = "{{table}}"
    try:
        merge_docx(source_path=source_path, content_path="", pattern=pattern)
    except ValueError as e:
        assert str(e) == "Content file path cannot be empty."
    else:
        raise AssertionError("Expected ValueError not raised.")


def test_merge_docx_with_source_not_docx_paths():
    source_path = "tests/fixtures/template.txt"
    content_path = "tests/fixtures/table.docx"
    pattern = "{{table}}"
    assert not Path(source_path).exists()
    assert Path(content_path).exists()
    # Test with invalid content path
    try:
        merge_docx(source_path=source_path, content_path=content_path, pattern=pattern)
    except ValueError as e:
        assert str(e) == "Source file must be a DOCX file."
    else:
        raise AssertionError("Expected ValueError not raised.")


def test_merge_docx_with_content_not_docx_paths():
    source_path = "tests/fixtures/template.docx"
    content_path = "tests/fixtures/table.txt"
    pattern = "{{table}}"
    assert Path(source_path).exists()
    assert not Path(content_path).exists()
    # Test with invalid content path
    try:
        merge_docx(source_path=source_path, content_path=content_path, pattern=pattern)
    except ValueError as e:
        assert str(e) == "Content file must be a DOCX file."
    else:
        raise AssertionError("Expected ValueError not raised.")


def test_merge_docx_with_output_not_docx_paths():
    source_path = "tests/fixtures/template.docx"
    content_path = "tests/fixtures/table.docx"
    output_path = "tests/fixtures/output.txt"
    pattern = "{{table}}"
    assert Path(source_path).exists()
    assert Path(content_path).exists()
    assert not Path(output_path).exists()
    # Test with invalid content path
    try:
        merge_docx(source_path=source_path, content_path=content_path, output_path=output_path, pattern=pattern)
    except ValueError as e:
        assert str(e) == "Output file must be a DOCX file."
    else:
        raise AssertionError("Expected ValueError not raised.")


def test_merge_docx_with_source_not_existing_paths():
    invalid_source_path = "tests/fixtures/invalid_template.docx"
    content_path = "tests/fixtures/table.docx"
    pattern = "{{table}}"
    assert Path(content_path).exists()
    assert not Path(invalid_source_path).exists()
    # Test with invalid source path
    try:
        merge_docx(source_path=invalid_source_path, content_path=content_path, pattern=pattern)
    except FileNotFoundError as e:
        assert str(e) == f"Source file {invalid_source_path} does not exist."
    else:
        raise AssertionError("Expected FileNotFoundError not raised.")


def test_merge_docx_with_content_not_existing_paths():
    source_path = "tests/fixtures/template.docx"
    invalid_content_path = "tests/fixtures/invalid_table.docx"
    pattern = "{{table}}"
    assert Path(source_path).exists()
    assert not Path(invalid_content_path).exists()
    # Test with invalid content path
    try:
        merge_docx(source_path=source_path, content_path=invalid_content_path, pattern=pattern)
    except FileNotFoundError as e:
        assert str(e) == f"Content file {invalid_content_path} does not exist."
    else:
        raise AssertionError("Expected FileNotFoundError not raised.")


def test_merge_docx_with_output_already_existing_paths():
    source_path = "tests/fixtures/template.docx"
    content_path = "tests/fixtures/table.docx"
    output_path = "tests/fixtures/template.docx"
    pattern = "{{table}}"
    assert Path(source_path).exists()
    assert Path(content_path).exists()
    assert Path(output_path).exists()
    # Test with invalid content path
    try:
        merge_docx(source_path=source_path, content_path=content_path, output_path=output_path, pattern=pattern)
    except FileExistsError as e:
        assert str(e) == f"Output file {output_path} already exists."
    else:
        raise AssertionError("Expected FileExistsError not raised.")


def test_merge_docx_with_no_pattern_or_insert_position():
    source_path = "tests/fixtures/template.docx"
    content_path = "tests/fixtures/table.docx"
    output_path = "tests/fixtures/output.docx"
    assert Path(source_path).exists()
    assert Path(content_path).exists()
    assert not Path(output_path).exists()

    # Test with no pattern or insert position
    try:
        merge_docx(source_path=source_path, content_path=content_path, output_path=output_path)
    except ValueError as e:
        assert str(e) == "At least one of pattern, insert_start, or insert_end must be specified."
    else:
        raise AssertionError("Expected ValueError not raised.")


def test_merge_docx_with_invalid_pattern():
    source_path = "tests/fixtures/template.docx"
    content_path = "tests/fixtures/table.docx"
    output_path = "tests/fixtures/output.docx"
    pattern = "{{invalid_pattern}}"
    assert Path(source_path).exists()
    assert Path(content_path).exists()
    assert not Path(output_path).exists()

    # Test with invalid pattern
    try:
        merge_docx(source_path=source_path, content_path=content_path, output_path=output_path, pattern=pattern)
    except ValueError as e:
        assert str(e) == "No pattern found in the target XML and no insert_start or insert_end specified."
    else:
        raise AssertionError("Expected ValueError not raised.")
