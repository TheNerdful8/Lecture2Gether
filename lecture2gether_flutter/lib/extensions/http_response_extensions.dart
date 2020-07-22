import 'package:http/http.dart' as http;

extension FollowRedirects on Future<http.Response> {
  Future<http.Response> followRedirects() =>
      this.then((response) {
        switch (response.statusCode) {
          case 301: // Moved permanently
          case 302: // Found (moved temporarily)
          case 303: // See other
            return this._repeatRequest(
                response.request, Uri.parse(response.headers['location']),
                newMethod: 'GET');
          case 307: // Temporary Redirect
          case 308: // Permanent Redirect
            return this._repeatRequest(
                response.request, Uri.parse(response.headers['location']));
          default:
            return response;
        }
      });

  Future<http.Response> _repeatRequest(http.Request original, Uri url,
      {String newMethod}) async {
    var request = http.Request(original.method, url);
    if (original.body.isNotEmpty)
      request.body = original.body;
    request.headers.addAll(original.headers);

    return http.Response.fromStream(await request.send());
  }
}
