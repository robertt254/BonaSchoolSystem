import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { downloadCsv } from './csvExport'

describe('downloadCsv', () => {
  let blobSpy

  beforeEach(() => {
    // Mock URL.createObjectURL and URL.revokeObjectURL
    global.URL.createObjectURL = vi.fn(() => 'blob:test-url')
    global.URL.revokeObjectURL = vi.fn()
    blobSpy = vi.spyOn(global, 'Blob')
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('should escape strings containing commas by wrapping them in double quotes', () => {
    const filename = 'test-file'
    const headers = [{ key: 'name', label: 'Name' }]
    const rows = [{ name: 'Smith, John' }]

    // Mock DOM elements to prevent error and test behavior
    const clickMock = vi.fn()
    const aMock = { href: '', download: '', click: clickMock }
    vi.spyOn(document, 'createElement').mockReturnValue(aMock)
    vi.spyOn(document.body, 'appendChild').mockImplementation(() => {})
    vi.spyOn(document.body, 'removeChild').mockImplementation(() => {})

    downloadCsv(filename, headers, rows)

    const blobArg = blobSpy.mock.calls[0][0][0]
    const bom = '\uFEFF'
    const expectedLines = [
      'Name',
      '"Smith, John"'
    ]
    expect(blobArg).toBe(bom + expectedLines.join('\r\n'))
  })

  it('should escape double quotes by doubling them and wrapping the field in double quotes', () => {
    const filename = 'test-file'
    const headers = [{ key: 'desc', label: 'Description' }]
    const rows = [{ desc: 'A "special" item' }]

    const clickMock = vi.fn()
    const aMock = { href: '', download: '', click: clickMock }
    vi.spyOn(document, 'createElement').mockReturnValue(aMock)
    vi.spyOn(document.body, 'appendChild').mockImplementation(() => {})
    vi.spyOn(document.body, 'removeChild').mockImplementation(() => {})

    downloadCsv(filename, headers, rows)

    const blobArg = blobSpy.mock.calls[0][0][0]
    const bom = '\uFEFF'
    const expectedLines = [
      'Description',
      '"A ""special"" item"'
    ]
    expect(blobArg).toBe(bom + expectedLines.join('\r\n'))
  })

  it('should escape strings containing newlines by wrapping them in double quotes', () => {
    const filename = 'test-file'
    const headers = [{ key: 'notes', label: 'Notes' }]
    const rows = [{ notes: 'Line 1\nLine 2' }]

    const clickMock = vi.fn()
    const aMock = { href: '', download: '', click: clickMock }
    vi.spyOn(document, 'createElement').mockReturnValue(aMock)
    vi.spyOn(document.body, 'appendChild').mockImplementation(() => {})
    vi.spyOn(document.body, 'removeChild').mockImplementation(() => {})

    downloadCsv(filename, headers, rows)

    const blobArg = blobSpy.mock.calls[0][0][0]
    const bom = '\uFEFF'
    const expectedLines = [
      'Notes',
      '"Line 1\nLine 2"'
    ]
    expect(blobArg).toBe(bom + expectedLines.join('\r\n'))
  })

  it('should replace null or undefined values with empty strings', () => {
    const filename = 'test-file'
    const headers = [
      { key: 'col1', label: 'Col1' },
      { key: 'col2', label: 'Col2' },
      { key: 'col3', label: 'Col3' }
    ]
    const rows = [
      { col1: null, col2: undefined, col3: 'Value' }
    ]

    const clickMock = vi.fn()
    const aMock = { href: '', download: '', click: clickMock }
    vi.spyOn(document, 'createElement').mockReturnValue(aMock)
    vi.spyOn(document.body, 'appendChild').mockImplementation(() => {})
    vi.spyOn(document.body, 'removeChild').mockImplementation(() => {})

    downloadCsv(filename, headers, rows)

    const blobArg = blobSpy.mock.calls[0][0][0]
    const bom = '\uFEFF'
    const expectedLines = [
      'Col1,Col2,Col3',
      ',,Value'
    ]
    expect(blobArg).toBe(bom + expectedLines.join('\r\n'))
  })

  it('should correctly escape headers as well if they contain special characters', () => {
    const filename = 'test-file'
    const headers = [{ key: 'col1', label: 'Col, 1' }]
    const rows = [{ col1: 'Value' }]

    const clickMock = vi.fn()
    const aMock = { href: '', download: '', click: clickMock }
    vi.spyOn(document, 'createElement').mockReturnValue(aMock)
    vi.spyOn(document.body, 'appendChild').mockImplementation(() => {})
    vi.spyOn(document.body, 'removeChild').mockImplementation(() => {})

    downloadCsv(filename, headers, rows)

    const blobArg = blobSpy.mock.calls[0][0][0]
    const bom = '\uFEFF'
    const expectedLines = [
      '"Col, 1"',
      'Value'
    ]
    expect(blobArg).toBe(bom + expectedLines.join('\r\n'))
  })
})

describe('downloadCsv DOM and file extension handling', () => {
  let blobSpy

  beforeEach(() => {
    // Mock URL.createObjectURL and URL.revokeObjectURL
    global.URL.createObjectURL = vi.fn(() => 'blob:test-url')
    global.URL.revokeObjectURL = vi.fn()
    blobSpy = vi.spyOn(global, 'Blob')
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('should append .csv to filename if not present', () => {
    const filename = 'my-export'
    const headers = [{ key: 'id', label: 'ID' }]
    const rows = [{ id: 1 }]

    const clickMock = vi.fn()
    const aMock = { href: '', download: '', click: clickMock }
    vi.spyOn(document, 'createElement').mockReturnValue(aMock)
    vi.spyOn(document.body, 'appendChild').mockImplementation(() => {})
    vi.spyOn(document.body, 'removeChild').mockImplementation(() => {})

    downloadCsv(filename, headers, rows)

    expect(aMock.download).toBe('my-export.csv')
  })

  it('should not append .csv to filename if already present', () => {
    const filename = 'my-export.csv'
    const headers = [{ key: 'id', label: 'ID' }]
    const rows = [{ id: 1 }]

    const clickMock = vi.fn()
    const aMock = { href: '', download: '', click: clickMock }
    vi.spyOn(document, 'createElement').mockReturnValue(aMock)
    vi.spyOn(document.body, 'appendChild').mockImplementation(() => {})
    vi.spyOn(document.body, 'removeChild').mockImplementation(() => {})

    downloadCsv(filename, headers, rows)

    expect(aMock.download).toBe('my-export.csv')
  })

  it('should trigger DOM elements appropriately to initiate download', () => {
    const filename = 'test-file'
    const headers = [{ key: 'id', label: 'ID' }]
    const rows = [{ id: 1 }]

    const clickMock = vi.fn()
    const aMock = { href: '', download: '', click: clickMock }
    const createElementSpy = vi.spyOn(document, 'createElement').mockReturnValue(aMock)
    const appendChildSpy = vi.spyOn(document.body, 'appendChild').mockImplementation(() => {})
    const removeChildSpy = vi.spyOn(document.body, 'removeChild').mockImplementation(() => {})

    downloadCsv(filename, headers, rows)

    expect(global.URL.createObjectURL).toHaveBeenCalled()
    expect(createElementSpy).toHaveBeenCalledWith('a')
    expect(aMock.href).toBe('blob:test-url')
    expect(appendChildSpy).toHaveBeenCalledWith(aMock)
    expect(clickMock).toHaveBeenCalled()
    expect(removeChildSpy).toHaveBeenCalledWith(aMock)
    expect(global.URL.revokeObjectURL).toHaveBeenCalledWith('blob:test-url')
  })
})
