import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Upload, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import './App.css'

function App() {
  const [selectedFiles, setSelectedFiles] = useState([])
  const [uploadStatus, setUploadStatus] = useState('')
  const [isUploading, setIsUploading] = useState(false)

  const handleFileSelect = (event) => {
    const files = Array.from(event.target.files)
    setSelectedFiles(files)
    setUploadStatus('')
  }

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      setUploadStatus('Please select files to upload.')
      return
    }

    setIsUploading(true)
    setUploadStatus('')

    // Simulate upload process for testing
    setTimeout(() => {
      setUploadStatus(`Successfully selected ${selectedFiles.length} file(s) for upload. AWS integration will be available after deployment.`)
      setSelectedFiles([])
      setIsUploading(false)
      
      // Reset file input
      const fileInput = document.getElementById('file-input')
      if (fileInput) fileInput.value = ''
    }, 2000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AWS S3 File Upload
          </h1>
          <p className="text-gray-600">
            Securely upload files to your S3 bucket
          </p>
        </div>

        {/* File Upload Card */}
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="w-5 h-5" />
              Upload Files
            </CardTitle>
            <CardDescription>
              Select files to upload to your S3 bucket. Existing files with the same name will be overwritten.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* File Input */}
            <div className="space-y-2">
              <Label htmlFor="file-input">Choose Files</Label>
              <Input
                id="file-input"
                type="file"
                multiple
                onChange={handleFileSelect}
                className="cursor-pointer"
                disabled={isUploading}
              />
            </div>

            {/* Selected Files Display */}
            {selectedFiles.length > 0 && (
              <div className="space-y-2">
                <Label>Selected Files ({selectedFiles.length})</Label>
                <div className="bg-gray-50 rounded-md p-3 max-h-32 overflow-y-auto">
                  {selectedFiles.map((file, index) => (
                    <div key={index} className="flex justify-between items-center py-1">
                      <span className="text-sm text-gray-700 truncate">{file.name}</span>
                      <span className="text-xs text-gray-500 ml-2">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Upload Button */}
            <Button 
              onClick={handleUpload} 
              disabled={selectedFiles.length === 0 || isUploading}
              className="w-full"
              size="lg"
            >
              {isUploading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4 mr-2" />
                  Select Files for Upload
                </>
              )}
            </Button>

            {/* Status Message */}
            {uploadStatus && (
              <Alert className={uploadStatus.includes('Successfully') ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}>
                {uploadStatus.includes('Successfully') ? (
                  <CheckCircle className="h-4 w-4 text-green-600" />
                ) : (
                  <AlertCircle className="h-4 w-4 text-red-600" />
                )}
                <AlertDescription className={uploadStatus.includes('Successfully') ? 'text-green-800' : 'text-red-800'}>
                  {uploadStatus}
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Info Card */}
        <Card className="mt-6 shadow-lg">
          <CardHeader>
            <CardTitle className="text-lg">How it works</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                Files will be uploaded directly to your AWS S3 bucket
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                Authentication will be handled by AWS Cognito
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                Files with the same name will be overwritten
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                All uploads are secure and private to your account
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* Development Notice */}
        <Card className="mt-6 shadow-lg border-yellow-200 bg-yellow-50">
          <CardHeader>
            <CardTitle className="text-lg text-yellow-800">Development Mode</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-yellow-700">
              This is the development version. AWS authentication and S3 upload functionality will be available after deploying the CDK stack and configuring the environment variables.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default App

