class Dashing.Graph extends Dashing.Widget

  @accessor 'current', ->
    return @get('displayedValue') if @get('displayedValue')
    points = @get('points')
    if points
      displaytotal[0].y
      displaytotal[0].x


  ready: ->
    container = $(@node).parent()
    # Gross hacks. Let's fix this.
    #data = @get('points') #if @get('points')
    width = (Dashing.widget_base_dimensions[0] * container.data("sizex")) + Dashing.widget_margins[0] * 2 * (container.data("sizex") - 1)
    height = (Dashing.widget_base_dimensions[1] * container.data("sizey"))
    @graph = new Rickshaw.Graph(
      element: @node
      width: width
      height: height
      renderer: 'line',
      series: [
        {
        color: "#fff",
        #data: data
        data: [{x:0, y:0}]
        }
      ]
    )

    @graph.series[0].data = @get('points') if @get('points') # points here..

    x_axis = new Rickshaw.Graph.Axis.X(graph: @graph, tickFormat: Rickshaw.Fixtures.Number.formatKMBT)
    y_axis = new Rickshaw.Graph.Axis.Y(graph: @graph, tickFormat: Rickshaw.Fixtures.Number.formatKMBT)
    @graph.render()


  onData: (data) ->
    if @graph
      #@graph.series[0].data = data.points
      @graph.render()
