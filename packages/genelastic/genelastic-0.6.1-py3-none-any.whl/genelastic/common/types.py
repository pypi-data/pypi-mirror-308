# pylint: disable=missing-module-docstring

import typing

Bucket: typing.TypeAlias = dict[str, dict[typing.Any, typing.Any]]

AnalysisMetaData: typing.TypeAlias = typing.Dict[str, str | int]
WetProcessesData: typing.TypeAlias = typing.Dict[str, str | int | float]
BioInfoProcessData: typing.TypeAlias = typing.Dict[str, str | typing.List[str]]
BundleDict: typing.TypeAlias = typing.Dict[str, typing.Any]

AnalysisDocument: typing.TypeAlias = typing.Dict[str, str | None | AnalysisMetaData]
MetadataDocument: typing.TypeAlias = typing.Dict[str, int | str | typing.List[typing.Any | None]]
ProcessDocument: typing.TypeAlias = (typing.Dict[str, str] |
                                     WetProcessesData |
                                     BioInfoProcessData)
BulkItems: typing.TypeAlias = typing.List[typing.Dict[str, str |
                                                           MetadataDocument |
                                                           AnalysisDocument |
                                                           ProcessDocument]]
