from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union
from uuid import UUID

@dataclass
class FstabEntry:
    filesystem: str
    mount: Optional[Path]
    fstype: str
    options: List[str]
    dump: int = 0
    pass_const: int = 0

    def __str__(self) -> str:
        return f'{self.filesystem} {self.mount or "none"} {self.fstype} {",".join(self.options)} {self.dump} {self.pass_const}'

class Fstab:
    def __init__(self, *, path:str = '/etc/fstab') -> None:
        self.__entries: List[Union[FstabEntry, str]] = []
        with open(path, 'r') as fstab_file:
            for line in fstab_file:
                if line.startswith('#'):
                    self.__entries.append(line.strip())
                    continue
                entry_data = line.split()
                filesystem = entry_data[0]
                if entry_data[1] == 'none':
                    mount = None
                else:
                    mount = Path(entry_data[1])
                fstype = entry_data[2]
                options = entry_data[3].split(',')
                dump = int(entry_data[4])
                pass_const = int(entry_data[5])

                self.__entries.append(FstabEntry(
                    filesystem=filesystem,
                    mount=mount,
                    fstype=fstype,
                    options=options,
                    dump=dump,
                    pass_const=pass_const
                ))

    @property
    def entries(self) -> List[FstabEntry]:
        return [entry for entry in self.__entries if isinstance(entry, FstabEntry)]

    def append(self, entry: FstabEntry) -> None:
        if entry not in self.__entries:
            self.__entries.append(entry)

    def compile(self, *, path='/etc/fstab') -> None:
        with open(path, 'w') as fstab_file:
            for entry in self.__entries:
                fstab_file.write(str(entry))
                fstab_file.write('\n')

        