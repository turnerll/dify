export async function GET() {
  try {
    // Simple health check for the frontend
    return Response.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: '222.place Web Frontend',
      version: '1.0.0'
    })
  } catch (error) {
    return Response.json(
      { 
        status: 'unhealthy', 
        error: 'Service unavailable' 
      },
      { status: 503 }
    )
  }
}