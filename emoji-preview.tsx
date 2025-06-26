export default function EmojiPreview() {
  return (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          Professional Emoji Preview for Audit Sampling Software
        </h1>
        <p className="text-gray-600">Compare different emoji styles for your application</p>
      </div>

      {/* Current vs Professional Header */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-red-500">
          <h2 className="text-xl font-semibold mb-4 text-red-600">Current Version</h2>
          <div className="bg-gradient-to-r from-purple-500 to-blue-600 text-white p-4 rounded-lg text-center">
            <h1 className="text-2xl font-bold">🎯 Modern Audit Sampling Software</h1>
            <p className="text-sm opacity-90">Professional audit sampling with modern UI/UX design</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-green-500">
          <h2 className="text-xl font-semibold mb-4 text-green-600">Professional Version</h2>
          <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-4 rounded-lg text-center">
            <h1 className="text-2xl font-bold">📊 Modern Audit Sampling Software</h1>
            <p className="text-sm opacity-90">Professional audit sampling with contemporary design</p>
          </div>
        </div>
      </div>

      {/* Navigation Menu Comparison */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-semibold mb-6 text-gray-800">Navigation Menu Comparison</h2>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Current */}
          <div className="space-y-3">
            <h3 className="font-semibold text-red-600 border-b pb-2">Current Emojis</h3>
            <div className="space-y-2">
              <div className="p-2 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer">🏠 Dashboard</div>
              <div className="p-2 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer">📁 File Upload</div>
              <div className="p-2 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer">👀 Data Preview</div>
              <div className="p-2 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer">⚙️ Sampling Config</div>
              <div className="p-2 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer">🎯 Sample Selection</div>
              <div className="p-2 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer">📊 Analysis & Evaluation</div>
              <div className="p-2 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer">📄 Reports & Export</div>
            </div>
          </div>

          {/* Professional */}
          <div className="space-y-3">
            <h3 className="font-semibold text-green-600 border-b pb-2">Professional Set</h3>
            <div className="space-y-2">
              <div className="p-2 bg-blue-50 rounded hover:bg-blue-100 cursor-pointer">📊 Dashboard</div>
              <div className="p-2 bg-blue-50 rounded hover:bg-blue-100 cursor-pointer">🗂️ Data Import</div>
              <div className="p-2 bg-blue-50 rounded hover:bg-blue-100 cursor-pointer">🔍 Data Review</div>
              <div className="p-2 bg-blue-50 rounded hover:bg-blue-100 cursor-pointer">🎛️ Configuration</div>
              <div className="p-2 bg-blue-50 rounded hover:bg-blue-100 cursor-pointer">📈 Sample Generation</div>
              <div className="p-2 bg-blue-50 rounded hover:bg-blue-100 cursor-pointer">📋 Analysis & Evaluation</div>
              <div className="p-2 bg-blue-50 rounded hover:bg-blue-100 cursor-pointer">📄 Reports & Export</div>
            </div>
          </div>

          {/* Minimalist */}
          <div className="space-y-3">
            <h3 className="font-semibold text-purple-600 border-b pb-2">Minimalist Set</h3>
            <div className="space-y-2">
              <div className="p-2 bg-purple-50 rounded hover:bg-purple-100 cursor-pointer">■ Dashboard</div>
              <div className="p-2 bg-purple-50 rounded hover:bg-purple-100 cursor-pointer">↑ Data Import</div>
              <div className="p-2 bg-purple-50 rounded hover:bg-purple-100 cursor-pointer">◉ Data Review</div>
              <div className="p-2 bg-purple-50 rounded hover:bg-purple-100 cursor-pointer">◈ Configuration</div>
              <div className="p-2 bg-purple-50 rounded hover:bg-purple-100 cursor-pointer">◆ Sample Generation</div>
              <div className="p-2 bg-purple-50 rounded hover:bg-purple-100 cursor-pointer">▣ Analysis & Evaluation</div>
              <div className="p-2 bg-purple-50 rounded hover:bg-purple-100 cursor-pointer">▤ Reports & Export</div>
            </div>
          </div>
        </div>
      </div>

      {/* Login Screen Comparison */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-semibold mb-6 text-gray-800">Login Screen Comparison</h2>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="border rounded-lg p-4">
            <h3 className="font-semibold text-red-600 mb-4">Current Login</h3>
            <div className="space-y-3">
              <h4 className="text-lg font-medium">🔐 Sign In</h4>
              <div className="space-y-2">
                <label className="block text-sm">👤 Username</label>
                <input className="w-full p-2 border rounded" placeholder="Enter username" />
                <label className="block text-sm">🔒 Password</label>
                <input className="w-full p-2 border rounded" type="password" placeholder="Enter password" />
                <button className="w-full bg-blue-600 text-white p-2 rounded">🚀 Sign In</button>
              </div>
            </div>
          </div>

          <div className="border rounded-lg p-4">
            <h3 className="font-semibold text-green-600 mb-4">Professional Login</h3>
            <div className="space-y-3">
              <h4 className="text-lg font-medium">🔐 Sign In</h4>
              <div className="space-y-2">
                <label className="block text-sm">👤 Username</label>
                <input className="w-full p-2 border rounded" placeholder="Enter username" />
                <label className="block text-sm">🔒 Password</label>
                <input className="w-full p-2 border rounded" type="password" placeholder="Enter password" />
                <button className="w-full bg-blue-600 text-white p-2 rounded">⚡ Sign In</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Dashboard Metrics Comparison */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-semibold mb-6 text-gray-800">Dashboard Metrics Comparison</h2>

        <div className="space-y-6">
          <div>
            <h3 className="font-semibold text-red-600 mb-3">Current Dashboard Cards</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white border rounded-lg p-4 text-center shadow-sm">
                <div className="text-sm font-medium text-gray-600">📁 Data Status</div>
                <div className="text-2xl font-bold text-blue-600 my-2">1,250</div>
                <div className="text-xs text-gray-500">Population Records</div>
              </div>
              <div className="bg-white border rounded-lg p-4 text-center shadow-sm">
                <div className="text-sm font-medium text-gray-600">🎯 Sample Size</div>
                <div className="text-2xl font-bold text-blue-600 my-2">125</div>
                <div className="text-xs text-gray-500">Items Selected</div>
              </div>
              <div className="bg-white border rounded-lg p-4 text-center shadow-sm">
                <div className="text-sm font-medium text-gray-600">⚠️ Risk Level</div>
                <div className="bg-green-500 text-white px-3 py-1 rounded-full text-sm my-2">Low</div>
                <div className="text-xs text-gray-500">Overall Assessment</div>
              </div>
              <div className="bg-white border rounded-lg p-4 text-center shadow-sm">
                <div className="text-sm font-medium text-gray-600">📋 Compliance</div>
                <div className="text-lg font-bold text-blue-600 my-2">ISA 530</div>
                <div className="text-xs text-gray-500">✅ Compliant</div>
              </div>
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-green-600 mb-3">Professional Dashboard Cards</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white border rounded-lg p-4 text-center shadow-sm">
                <div className="text-sm font-medium text-gray-600">📊 Data Status</div>
                <div className="text-2xl font-bold text-blue-600 my-2">1,250</div>
                <div className="text-xs text-gray-500">Population Records</div>
              </div>
              <div className="bg-white border rounded-lg p-4 text-center shadow-sm">
                <div className="text-sm font-medium text-gray-600">📈 Sample Size</div>
                <div className="text-2xl font-bold text-blue-600 my-2">125</div>
                <div className="text-xs text-gray-500">Items Selected</div>
              </div>
              <div className="bg-white border rounded-lg p-4 text-center shadow-sm">
                <div className="text-sm font-medium text-gray-600">🎯 Risk Level</div>
                <div className="bg-green-500 text-white px-3 py-1 rounded-full text-sm my-2">Low</div>
                <div className="text-xs text-gray-500">Overall Assessment</div>
              </div>
              <div className="bg-white border rounded-lg p-4 text-center shadow-sm">
                <div className="text-sm font-medium text-gray-600">📋 Compliance</div>
                <div className="text-lg font-bold text-blue-600 my-2">ISA 530</div>
                <div className="text-xs text-gray-500">✅ Compliant</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons Comparison */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-semibold mb-6 text-gray-800">Action Buttons Comparison</h2>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-red-600 mb-3">Current Buttons</h3>
            <div className="space-y-3">
              <button className="w-full bg-blue-600 text-white p-3 rounded-lg">📁 Upload New Data</button>
              <button className="w-full bg-gray-600 text-white p-3 rounded-lg">⚙️ Configure Sampling</button>
              <button className="w-full bg-green-600 text-white p-3 rounded-lg">📄 Generate Report</button>
              <button className="w-full bg-purple-600 text-white p-3 rounded-lg">➡️ Continue to Analysis</button>
              <button className="w-full bg-red-600 text-white p-3 rounded-lg">🚪 Logout</button>
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-green-600 mb-3">Professional Buttons</h3>
            <div className="space-y-3">
              <button className="w-full bg-blue-600 text-white p-3 rounded-lg">📤 Upload New Data</button>
              <button className="w-full bg-gray-600 text-white p-3 rounded-lg">🎛️ Configure Sampling</button>
              <button className="w-full bg-green-600 text-white p-3 rounded-lg">📋 Generate Report</button>
              <button className="w-full bg-purple-600 text-white p-3 rounded-lg">⚡ Continue to Analysis</button>
              <button className="w-full bg-red-600 text-white p-3 rounded-lg">🔐 Logout</button>
            </div>
          </div>
        </div>
      </div>

      {/* Status Indicators Comparison */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-semibold mb-6 text-gray-800">Status Indicators Comparison</h2>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-red-600 mb-3">Current Status Badges</h3>
            <div className="space-y-2">
              <span className="inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                ✅ Data Loaded
              </span>
              <span className="inline-block bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
                ⏳ Config Pending
              </span>
              <span className="inline-block bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">
                ❌ Error Occurred
              </span>
              <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                🔄 Processing
              </span>
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-green-600 mb-3">Professional Status Badges</h3>
            <div className="space-y-2">
              <span className="inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                ✅ Data Loaded
              </span>
              <span className="inline-block bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
                ⚠️ Config Pending
              </span>
              <span className="inline-block bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">
                ⚠️ Error Occurred
              </span>
              <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                🔄 Processing
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
        <h2 className="text-2xl font-semibold mb-4 text-blue-800">💡 Recommendations</h2>

        <div className="grid md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h3 className="font-semibold text-green-600 mb-2">✅ Professional Set</h3>
            <p className="text-sm text-gray-600">
              Best balance of professionalism and visual appeal. Suitable for corporate environments.
            </p>
          </div>

          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h3 className="font-semibold text-purple-600 mb-2">◆ Minimalist Set</h3>
            <p className="text-sm text-gray-600">
              Ultra-professional with geometric symbols. Perfect for formal audit environments.
            </p>
          </div>

          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h3 className="font-semibold text-blue-600 mb-2">🎯 Hybrid Approach</h3>
            <p className="text-sm text-gray-600">
              Mix professional emojis with geometric symbols for optimal user experience.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
