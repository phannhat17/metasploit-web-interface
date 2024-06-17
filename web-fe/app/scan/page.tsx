'use client';

import { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import { BeatLoader } from 'react-spinners';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { toast } from "sonner"

const StartScan: React.FC = () => {
  const [ipRange, setIpRange] = useState<string>('');
  const [autoScanServices, setAutoScanServices] = useState<boolean>(false);
  const [autoScanOs, setAutoScanOs] = useState<boolean>(false);
  const [message, setMessage] = useState<string>('');
  const [isSuccess, setIsSuccess] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setMessage('');
    setLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:5000/scan/start_scan', {
        ip_range: ipRange,
        auto_scan_services: autoScanServices,
        auto_scan_os: autoScanOs,
      });
      setLoading(false);
      if (response.data.success) {
        toast.success(response.data.success)
      } else {
        toast.error(response.data.error)
      }
    } catch (error: any) {
      setLoading(false);
      toast.error(error.response?.data?.error || 'Error occurred')
    }
  };

  const handleCheckboxChange =
    (setter: React.Dispatch<React.SetStateAction<boolean>>) => (checked: boolean) => {
      setter(checked);
    };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-full max-w-lg mx-2 shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">Start Scan</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">IP Range</label>
              <Input
                value={ipRange}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setIpRange(e.target.value)}
                required
                className="mt-1 block w-full"
              />
            </div>
            <div className="flex items-center">
              <Checkbox
                checked={autoScanServices}
                onCheckedChange={handleCheckboxChange(setAutoScanServices)}
                id="auto-scan-services"
              />
              <label htmlFor="auto-scan-services" className="ml-2 block text-sm text-gray-900">
                Auto Scan Services
              </label>
            </div>
            <div className="flex items-center">
              <Checkbox
                checked={autoScanOs}
                onCheckedChange={handleCheckboxChange(setAutoScanOs)}
                id="auto-scan-os"
              />
              <label htmlFor="auto-scan-os" className="ml-2 block text-sm text-gray-900">
                Auto Scan OS
              </label>
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Scanning...' : 'Start Scan'}
            </Button>
          </form>
        </CardContent>
        {loading && (
          <CardFooter>
            <BeatLoader className="m-auto" />
          </CardFooter>
        )}
      </Card>
    </div>
  );
};

export default StartScan;
