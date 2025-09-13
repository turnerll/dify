export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-12">
      <div className="max-w-4xl mx-auto text-center px-4">
        <h1 className="text-6xl font-bold text-gray-900 mb-6">
          Welcome to <span className="text-blue-600">222.place</span>
        </h1>
        
        <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto">
          A privacy-first matchmaking platform that connects people through shared interests, 
          activities, and local events. Find your community, discover new experiences, 
          and build meaningful connections.
        </p>

        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="text-3xl mb-4">🎯</div>
            <h3 className="text-lg font-semibold mb-2">Smart Matching</h3>
            <p className="text-gray-600">Advanced algorithm matches you with compatible people based on interests, values, and preferences.</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="text-3xl mb-4">🎉</div>
            <h3 className="text-lg font-semibold mb-2">Local Events</h3>
            <p className="text-gray-600">Discover dinners, gatherings, and activities happening in your area with like-minded people.</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="text-3xl mb-4">🔒</div>
            <h3 className="text-lg font-semibold mb-2">Privacy First</h3>
            <p className="text-gray-600">Your data stays yours. Self-hosted, open-source, and designed with privacy in mind.</p>
          </div>
        </div>

        <div className="space-x-4">
          <button className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
            Get Started
          </button>
          <button className="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
            Learn More
          </button>
        </div>

        <div className="mt-16 pt-8 border-t border-gray-200">
          <p className="text-sm text-gray-500">
            🌟 Bilingual support (English/Spanish) • 🏠 Self-hosted • 🔓 Open source
          </p>
        </div>
      </div>
    </div>
  )
}