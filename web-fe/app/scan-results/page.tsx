'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Dialog, DialogOverlay, DialogContent, DialogHeader, DialogTitle, DialogClose } from '@/components/ui/dialog';
import { toast } from "sonner"

const ScanResults: React.FC = () => {
  const [targets, setTargets] = useState<any[]>([]);
  const [selectedTarget, setSelectedTarget] = useState<string>('');
  const [scans, setScans] = useState<any[]>([]);
  const [selectedScan, setSelectedScan] = useState<any>(null);
  const [scriptDetails, setScriptDetails] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false);

  useEffect(() => {
    fetchTargets();
  }, []);

  const fetchTargets = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await axios.get('http://127.0.0.1:5000/scan-results/all-record');
      setTargets(response.data.directories);
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Error occurred')
    }
    setLoading(false);
  };

  const fetchScans = async (ip: string) => {
    setLoading(true);
    setError('');
    setScans([]);
    setSelectedScan(null);

    try {
      const response = await axios.get('http://127.0.0.1:5000/scan-results/all-record', {
        params: { ip },
      });
      setScans(response.data.records);
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Error occurred')
    }
    setLoading(false);
  };

  const fetchScanDetails = async (ip: string, timestamp: string) => {
    setLoading(true);
    setError('');
    setSelectedScan(null);
    setScriptDetails(null);

    try {
      const response = await axios.get('http://127.0.0.1:5000/scan-results', {
        params: {
          ip,
          timestamp,
          resulttype: 'port',
        },
      });
      setSelectedScan(response.data);
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Error occurred')
    }
    setLoading(false);
  };

  const fetchScriptDetails = async (ip: string, timestamp: string, portid: string) => {
    setLoading(true);
    setError('');
    setScriptDetails(null);

    try {
      const response = await axios.get('http://127.0.0.1:5000/scan-results/script-details', {
        params: {
          ip,
          timestamp,
          portid,
        },
      });
      setScriptDetails(response.data);
      setIsDialogOpen(true);
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Error occurred');
    }
    setLoading(false);
  };

  const renderScriptDetailsTable = () => {
    if (!scriptDetails) return null;

    const tableData = scriptDetails.table?.table || [];

    return (
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b">ID</th>
            <th className="py-2 px-4 border-b">CVSS</th>
            <th className="py-2 px-4 border-b">Type</th>
            <th className="py-2 px-4 border-b">Is Exploit</th>
          </tr>
        </thead>
        <tbody>
          {tableData.map((item: any, index: number) => (
            <tr key={index}>
              <td className="py-2 px-4 border-b">{item.elem.find((e: any) => e['@key'] === 'id')?.['#text']}</td>
              <td className="py-2 px-4 border-b">{item.elem.find((e: any) => e['@key'] === 'cvss')?.['#text']}</td>
              <td className="py-2 px-4 border-b">{item.elem.find((e: any) => e['@key'] === 'type')?.['#text']}</td>
              <td className="py-2 px-4 border-b">{item.elem.find((e: any) => e['@key'] === 'is_exploit')?.['#text']}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <Card className="w-full max-w-4xl shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">Scan Results</CardTitle>
        </CardHeader>
        <CardContent>
          {loading && <p className="text-center">Loading...</p>}
          {/* {error && <p className="text-center text-red-500">{error}</p>} */}
          {!loading && !error && targets.length === 0 && (
            <p className="text-center">No targets available.</p>
          )}
          {!loading && !error && targets.length > 0 && (
            <div className="space-y-4">
              <div>
                <h3 className="text-xl font-semibold mb-2">Targets</h3>
                <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {targets.map((target) => (
                    <li key={target.ip} className="border p-4 rounded-lg shadow-sm bg-white">
                      <button
                        onClick={() => {
                          setSelectedTarget(target.ip);
                          fetchScans(target.ip);
                        }}
                        className="text-blue-500 hover:underline"
                      >
                        {target.ip} ({target.scans} scans)
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
              {selectedTarget && scans.length > 0 && (
                <div>
                  <h3 className="text-xl font-semibold mb-2">Scans for {selectedTarget}</h3>
                  <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {scans.map((scan) => (
                      <li key={scan.timestamp} className="border p-4 rounded-lg shadow-sm bg-white">
                        <button
                          onClick={() => fetchScanDetails(selectedTarget, scan.timestamp)}
                          className="text-blue-500 hover:underline"
                        >
                          {scan.formatted_time}
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {selectedScan && (
                <div>
                  <h3 className="text-xl font-semibold mb-2">Scan Details</h3>
                  <div className="bg-gray-200 p-4 rounded-lg shadow-inner">
                    <ul>
                      {selectedScan.ports.map((port: any) => (
                        <li key={port["@portid"]} className="mb-4">
                          <div className="border p-4 rounded-lg shadow-sm bg-white">
                            <p><strong>Port ID:</strong> {port["@portid"]}</p>
                            <p><strong>Product:</strong> {port.service["@product"] || 'N/A'}</p>
                            <p><strong>Version:</strong> {port.service["@version"] || 'N/A'}</p>
                            <button
                              onClick={async () => {
                                await fetchScriptDetails(selectedTarget, selectedScan.timestamp, port["@portid"]);
                                setIsDialogOpen(true);
                              }}
                              className="text-blue-500 hover:underline"
                            >
                              View Script Details
                            </button>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
      {isDialogOpen && (
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent className="sm:max-w-5xl overflow-auto max-h-screen">
            <DialogHeader>
              <DialogTitle>Script Details</DialogTitle>
              <DialogClose onClick={() => setIsDialogOpen(false)} />
            </DialogHeader>
            <div className="bg-gray-200 p-4 rounded-lg shadow-inner">
              {scriptDetails ? (
                <>
                  <table className="min-w-full bg-white">
                    <thead>
                      <tr>
                        <th className="py-2 px-4 border-b">ID</th>
                        <th className="py-2 px-4 border-b">CVSS</th>
                        <th className="py-2 px-4 border-b">Type</th>
                        <th className="py-2 px-4 border-b">Is Exploit</th>
                      </tr>
                    </thead>
                    <tbody>
                      {scriptDetails.table?.table.map((item: any, index: number) => (
                        <tr key={index}>
                          <td className="py-2 px-4 border-b">{item.elem.find((e: any) => e['@key'] === 'id')?.['#text']}</td>
                          <td className="py-2 px-4 border-b">{item.elem.find((e: any) => e['@key'] === 'cvss')?.['#text']}</td>
                          <td className="py-2 px-4 border-b">{item.elem.find((e: any) => e['@key'] === 'type')?.['#text']}</td>
                          <td className="py-2 px-4 border-b">{item.elem.find((e: any) => e['@key'] === 'is_exploit')?.['#text']}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </>
              ) : (
                <p>No details available.</p>
              )}
            </div>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
};

export default ScanResults;
