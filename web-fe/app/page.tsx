'use client';

import { useState } from 'react';
import axios from 'axios';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Dialog, DialogOverlay, DialogContent, DialogHeader, DialogTitle, DialogClose } from '@/components/ui/dialog';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
} from '@tanstack/react-table';
import { toast } from "sonner"

const Index: React.FC = () => {
  const [name, setName] = useState<string>('');
  const [type, setType] = useState<string>('all');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false);
  const [moduleDetails, setModuleDetails] = useState<any>(null);

  const handleSearch = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://127.0.0.1:5000/', { name, type });
      setResults(response.data.rows);
      if (response.data.toast) {
        toast.error('No results found');
      }
      if (response.data.toast2) {
        toast.warning('Please specify a module type');
      }
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Error occurred');
    }
    setLoading(false);
  };

  const stripTypeFromFullName = (fullname: string, type: string) => {
    const typePrefix = `${type}/`;
    if (fullname.startsWith(typePrefix)) {
      return fullname.slice(typePrefix.length);
    }
    return fullname;
  };

  const handleUseModule = () => {
    if (moduleDetails) {
      const parts = moduleDetails.fullname.split('/');
      const moduleType = parts[0];
      const moduleName = parts.slice(1).join('/');
      window.location.href = `/exploit/options?type=${moduleType}&name=${moduleName}`;
    }
  };

  const fetchModuleDetails = async (moduleType: string, moduleFullName: string) => {
    const strippedFullName = stripTypeFromFullName(moduleFullName, moduleType);

    setLoading(true);
    setError('');

    try {
      const response = await axios.get('http://127.0.0.1:5000/module_details', {
        params: { module_type: moduleType, module_name: strippedFullName },
      });
      setModuleDetails(response.data);
      setIsDialogOpen(true);
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Error occurred');
    }
    setLoading(false);
  };

  const columns: ColumnDef<any>[] = [
    {
      accessorKey: 'name',
      header: 'Name',
    },
    {
      accessorKey: 'type',
      header: 'Type',
    },
    {
      accessorKey: 'rank',
      header: 'Rank',
    },
    {
      accessorKey: 'disclosuredate',
      header: 'Disclosure Date',
    },
    {
      id: 'action',
      header: 'Action',
      cell: ({ row }) => (
        <button
          onClick={() => fetchModuleDetails(row.original.type, row.original.fullname)}
          className="text-blue-500 hover:underline"
        >
          View Details
        </button>
      ),
    },
  ];

  const table = useReactTable({
    data: results,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <Card className="w-full max-w-5xl shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">Search Modules</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <Input
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="mt-1 block w-full"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Type</label>
              <select
                value={type}
                onChange={(e) => setType(e.target.value)}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="all">All</option>
                <option value="exploit">Exploit</option>
                <option value="auxiliary">Auxiliary</option>
                <option value="post">Post</option>
                <option value="payload">Payload</option>
                <option value="encoder">Encoder</option>
                <option value="nop">NOP</option>
              </select>
            </div>
            <Button type="submit" className="w-full">
              Search
            </Button>
          </form>
          {/* {loading && <p className="text-center">Loading...</p>}
          {error && <p className="text-center text-red-500">{error}</p>} */}
          {results.length > 0 && (
            <div className="mt-4">
              <h3 className="text-xl font-semibold mb-2">Results</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full bg-white border border-gray-200">
                  <thead className="bg-gray-50">
                    {table.getHeaderGroups().map(headerGroup => (
                      <tr key={headerGroup.id}>
                        {headerGroup.headers.map(header => (
                          <th
                            key={header.id}
                            className="px-6 py-3 border-b-2 border-gray-300 text-left text-sm font-medium text-gray-700 tracking-wider"
                          >
                            {header.isPlaceholder ? null : (
                              <div
                                {...{
                                  className: header.column.getCanSort()
                                    ? 'cursor-pointer select-none'
                                    : '',
                                  onClick: header.column.getToggleSortingHandler(),
                                }}
                              >
                                {flexRender(
                                  header.column.columnDef.header,
                                  header.getContext()
                                )}
                                {{
                                  asc: ' ↑',
                                  desc: ' ↓',
                                }[header.column.getIsSorted() as string] ?? null}
                              </div>
                            )}
                          </th>
                        ))}
                      </tr>
                    ))}
                  </thead>
                  <tbody className="bg-white">
                    {table.getRowModel().rows.map(row => (
                      <tr key={row.id} className="hover:bg-gray-50">
                        {row.getVisibleCells().map(cell => (
                          <td key={cell.id} className="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                            {flexRender(cell.column.columnDef.cell, cell.getContext())}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
      {isDialogOpen && (
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent className="max-w-xl w-full">
            <DialogHeader>
              <DialogTitle>Module Details</DialogTitle>
              <DialogClose onClick={() => setIsDialogOpen(false)} />
            </DialogHeader>
            <div className="bg-gray-200 p-4 rounded-lg shadow-inner max-h-96 overflow-y-auto">
              {moduleDetails ? (
                <>
                  <p><strong>Module:</strong> {moduleDetails.name}</p>
                  <p><strong>Provided by:</strong> {moduleDetails.authors.join(', ')}</p>
                  <p><strong>Rank:</strong> {moduleDetails.rank}</p>
                  <p><strong>Disclosure:</strong> {moduleDetails.disclosuredate || 'No record'}</p>
                  <p><strong>Description:</strong> {moduleDetails.description}</p>
                  <p><strong>References:</strong></p>
                  {moduleDetails.references && moduleDetails.references.length > 0 && (
                    <div>
                      {moduleDetails.references.map((ref: [string, string], index: number) => (
                        <div key={index}>
                          {ref[1].startsWith('http://') || ref[1].startsWith('https://') ? (
                            <a href={ref[1]} target="_blank" className="font-medium text-blue-600 dark:text-blue-500 hover:underline">{ref[0]}: {ref[1]}</a>
                          ) : (
                            <div>{ref[0]}: {ref[1]}</div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <p>No details available.</p>
              )}
            </div>
            <div className="mt-4">
              <Button onClick={handleUseModule} className="w-full">Use Module</Button>
            </div>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
};

export default Index;