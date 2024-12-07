import asyncio

import bs4
import httpx

from src.ctp_pipeline_viewer.data_types import (
    CtpSummary,
    CtpStatus,
    RegexIn,
    DirectoryImportService,
    DicomFilter,
    IDMap,
    DicomAnonymizer,
    DicomExportService,
    PerformanceLogger,
)


async def get_ctp_summary(urls: list[str]) -> list[CtpSummary]:
    def _get_header(_table: bs4.Tag) -> list[str]:
        _header = []
        header_row = _table.find_all('tr')[0]
        for cell in header_row.find_all('th'):
            _header.append(cell.text)
        return _header

    def _get_data(_table: bs4.Tag) -> list[CtpSummary]:
        _header = _get_header(_table)
        _results = []
        for _row in _table.find_all('tr'):
            td = _row.find_all('td')
            if len(td) == 0:
                continue

            _results.append(CtpSummary(**dict(zip(_header, [cell.text for cell in td]))))
        return _results

    results = []
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            responses = await asyncio.gather(*[client.get(url) for url in urls])

            for response in responses:
                soup = bs4.BeautifulSoup(response.content, 'html.parser')
                tables = soup.find_all('table', attrs={'class': 'summary'})

                if len(tables) != 1:
                    continue

                results.extend(_get_data(tables[0]))
    except httpx.TransportError:
        print('Timeout')

    return results


async def get_ctp_status(urls: list[str]) -> list[CtpStatus]:
    def html_table_to_dict(_table: list[bs4.Tag]) -> dict[str, str]:
        return {_row.contents[0].text: _row.contents[1].text for _row in _table}

    async with httpx.AsyncClient(timeout=20) as client:
        responses = await asyncio.gather(*[client.get(url) for url in urls])

    pipelines: list[CtpStatus] = []
    for response in responses:
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        pipeline = None
        for tag in soup.body.contents:
            if tag.name == 'h2':
                if pipeline is not None:
                    pipelines.append(pipeline)
                pipeline = CtpStatus(name=tag.string)

            if tag.name == 'h3':
                assert pipeline
                table = html_table_to_dict(tag.nextSibling.contents)
                match RegexIn(tag.text):
                    case 'DirectoryImportService':
                        pipeline.elements.append(DirectoryImportService(**table))
                    case 'DicomFilter':
                        pipeline.elements.append(DicomFilter(**table))
                    case 'IDMap':
                        pipeline.elements.append(IDMap(**table))
                    case r'DicomAnonymizer\W?(?P<name>\w+)?' as m:
                        table['name'] = m['name']
                        pipeline.elements.append(DicomAnonymizer(**table))
                    case 'DicomExportService':
                        pipeline.elements.append(DicomExportService(**table))
                    case 'PerformanceLogger':
                        pipeline.elements.append(PerformanceLogger(**table))
                    case _:
                        print(f'UNKNOWN {tag.text}')

        if pipeline is not None:
            pipelines.append(pipeline)
    return pipelines
