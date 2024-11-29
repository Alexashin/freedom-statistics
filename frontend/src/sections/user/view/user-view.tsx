import { useState, useCallback } from 'react';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Table from '@mui/material/Table';
import Button from '@mui/material/Button';
import TableBody from '@mui/material/TableBody';
import Typography from '@mui/material/Typography';
import TableContainer from '@mui/material/TableContainer';
import TablePagination from '@mui/material/TablePagination';

import { _users } from 'src/_mock';
import { DashboardContent } from 'src/layouts/dashboard';

import { Iconify } from 'src/components/iconify';
import { Scrollbar } from 'src/components/scrollbar';

import { TableNoData } from '../table-no-data';
import { UserTableRow } from '../user-table-row';
import { UserTableHead } from '../user-table-head';
import { TableEmptyRows } from '../table-empty-rows';
import { UserTableToolbar } from '../user-table-toolbar';
import { emptyRows, applyFilter, getComparator } from '../utils';

import type { UserProps } from '../user-table-row';

// ----------------------------------------------------------------------

export function UserView() {
  const table = useTable();

  const [filterName, setFilterName] = useState('');

  const dataFiltered: UserProps[] = applyFilter({
    inputData: _users,
    comparator: getComparator(table.order, table.orderBy),
    filterName,
  });

  const notFound = !dataFiltered.length && !!filterName;

  return (
    <DashboardContent>
      <Box sx={{ mb: 6 }}>
        <Typography variant="h4" flexGrow={1}>
          Связь пакетов и каналов
        </Typography>
        <Card>
        <Scrollbar>
          <TableContainer>
            <Table sx={{ minWidth: 600 }}>
            <UserTableHead
                  order={table.order}
                  orderBy={table.orderBy}
                  rowCount={_users.length}
                  numSelected={table.selected.length}
                  onSort={table.onSort}
                  onSelectAllRows={(checked) =>
                    table.onSelectAllRows(
                      checked,
                      _users.map((user) => user.id)
                    )
                  }
                  headLabel={[
                  { id: 'packageName', label: 'Название пакета' },
                  { id: 'channelId', label: 'ID канала' },
                ]}
              />
          
            </Table>
          </TableContainer>
        </Scrollbar>
        <TablePagination
          component="div"
          page={table.page}
          count={dataFiltered.length}
          rowsPerPage={table.rowsPerPage}
          onPageChange={table.onChangePage}
          rowsPerPageOptions={[5, 10, 25]}
          onRowsPerPageChange={table.onChangeRowsPerPage}
        />
      </Card>
    </Box>


    <Box sx={{ mb: 6 }}>
      <Typography variant="h4" flexGrow={1}>
        Информация о клиентах 
      </Typography>
      <Card>
      <Scrollbar>
        <TableContainer>
          <Table sx={{ minWidth: 600 }}>
          <UserTableHead
                order={table.order}
                orderBy={table.orderBy}
                rowCount={_users.length}
                numSelected={table.selected.length}
                onSort={table.onSort}
                onSelectAllRows={(checked) =>
                  table.onSelectAllRows(
                    checked,
                    _users.map((user) => user.id)
                  )
                }
                headLabel={[
                { id: 'packageName', label: 'ID клиента' },
                { id: 'channelId', label: 'Андрес' },
                { id: 'channelId', label: 'Пол' },
                { id: 'channelId', label: 'Возрастной диапозон' },
              ]}
            />
        
            </Table>
          </TableContainer>
        </Scrollbar>
        <TablePagination
          component="div"
          page={table.page}
          count={dataFiltered.length}
          rowsPerPage={table.rowsPerPage}
          onPageChange={table.onChangePage}
          rowsPerPageOptions={[5, 10, 25]}
          onRowsPerPageChange={table.onChangeRowsPerPage}
        />
      </Card>
    </Box>

    <Box sx={{ mb: 6 }}>
      <Typography variant="h4" flexGrow={1}>
        Информация о домах
      </Typography>
      <Card>
      <Scrollbar>
        <TableContainer>
          <Table sx={{ minWidth: 600 }}>
          <UserTableHead
                order={table.order}
                orderBy={table.orderBy}
                rowCount={_users.length}
                numSelected={table.selected.length}
                onSort={table.onSort}
                onSelectAllRows={(checked) =>
                  table.onSelectAllRows(
                    checked,
                    _users.map((user) => user.id)
                  )
                }
                headLabel={[
                { id: 'packageName', label: 'Адрес' },
                { id: 'channelId', label: 'Кол-во квартир' },
                { id: 'channelId', label: 'Кол-во подъездов' },
                { id: 'channelId', label: 'Кол-во этажей' },
              ]}
            />
        
            </Table>
          </TableContainer>
        </Scrollbar>
        <TablePagination
          component="div"
          page={table.page}
          count={dataFiltered.length}
          rowsPerPage={table.rowsPerPage}
          onPageChange={table.onChangePage}
          rowsPerPageOptions={[5, 10, 25]}
          onRowsPerPageChange={table.onChangeRowsPerPage}
        />
      </Card>
    </Box>



    <Box sx={{ mb: 6 }}>
      <Typography variant="h4" flexGrow={1}>
        Статистика просмотров телепередач
      </Typography>
      <Card>
      <Scrollbar>
        <TableContainer>
          <Table sx={{ minWidth: 600 }}>
          <UserTableHead
                order={table.order}
                orderBy={table.orderBy}
                rowCount={_users.length}
                numSelected={table.selected.length}
                onSort={table.onSort}
                onSelectAllRows={(checked) =>
                  table.onSelectAllRows(
                    checked,
                    _users.map((user) => user.id)
                  )
                }
                headLabel={[
                { id: 'packageName', label: 'ID клиента' },
                { id: 'channelId', label: 'ID устройства' },
                { id: 'channelId', label: 'Выбор канала' },
                { id: 'channelId', label: 'ID канала' },
                { id: 'channelId', label: 'Название канала' },
                { id: 'channelId', label: 'Время начала программы' },
                { id: 'channelId', label: 'Время окончания программы' },
                { id: 'channelId', label: 'Продолжительность сеанса' },
                { id: 'channelId', label: 'Категория' },
                { id: 'channelId', label: 'Подкатегория' },
              ]}
            />
        
          </Table>
        </TableContainer>
      </Scrollbar>
      <TablePagination
        component="div"
        page={table.page}
        count={dataFiltered.length}
        rowsPerPage={table.rowsPerPage}
        onPageChange={table.onChangePage}
        rowsPerPageOptions={[5, 10, 25]}
        onRowsPerPageChange={table.onChangeRowsPerPage}
      />
    </Card>
  </Box>

    
    </DashboardContent>
  );
}

// ----------------------------------------------------------------------

export function useTable() {
  const [page, setPage] = useState(0);
  const [orderBy, setOrderBy] = useState('name');
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [selected, setSelected] = useState<string[]>([]);
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');

  const onSort = useCallback(
    (id: string) => {
      const isAsc = orderBy === id && order === 'asc';
      setOrder(isAsc ? 'desc' : 'asc');
      setOrderBy(id);
    },
    [order, orderBy]
  );

  const onSelectAllRows = useCallback((checked: boolean, newSelecteds: string[]) => {
    if (checked) {
      setSelected(newSelecteds);
      return;
    }
    setSelected([]);
  }, []);

  const onSelectRow = useCallback(
    (inputValue: string) => {
      const newSelected = selected.includes(inputValue)
        ? selected.filter((value) => value !== inputValue)
        : [...selected, inputValue];

      setSelected(newSelected);
    },
    [selected]
  );

  const onResetPage = useCallback(() => {
    setPage(0);
  }, []);

  const onChangePage = useCallback((event: unknown, newPage: number) => {
    setPage(newPage);
  }, []);

  const onChangeRowsPerPage = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setRowsPerPage(parseInt(event.target.value, 10));
      onResetPage();
    },
    [onResetPage]
  );

  return {
    page,
    order,
    onSort,
    orderBy,
    selected,
    rowsPerPage,
    onSelectRow,
    onResetPage,
    onChangePage,
    onSelectAllRows,
    onChangeRowsPerPage,
  };
}
