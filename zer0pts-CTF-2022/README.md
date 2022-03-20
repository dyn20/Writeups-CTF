# GitFile Explorer

There are five variables receive values from 5 parameters, when we enter values for these parameter, server will concat these value to valid URL by craft_url function (if we don't enter value for them, they will be set automatically.

```
$service = empty($_GET['service']) ? "" : $_GET['service'];
$owner   = empty($_GET['owner'])   ? "ptr-yudai" : $_GET['owner'];
$repo    = empty($_GET['repo'])    ? "ptrlib"    : $_GET['repo'];
$branch  = empty($_GET['branch'])  ? "master"    : $_GET['branch'];
$file    = empty($_GET['file'])    ? "README.md" : $_GET['file'];
```

```
function craft_url($service, $owner, $repo, $branch, $file) {
    if (strpos($service, "github") !== false) {
        /* GitHub URL */
        return $service."/".$owner."/".$repo."/".$branch."/".$file;

    } else if (strpos($service, "gitlab") !== false) {
        /* GitLab URL */
        return $service."/".$owner."/".$repo."/-/raw/".$branch."/".$file;

    } else if (strpos($service, "bitbucket") !== false) {
        /* BitBucket URL */
        return $service."/".$owner."/".$repo."/raw/".$branch."/".$file;

    }

    return null;
}
```
After these values are concated into a url, this url will be check with below condition, if it passes the condition, file_get_contents will be called:

```
if ($service) {
    $url = craft_url($service, $owner, $repo, $branch, $file);
    if (preg_match("/^http.+\/\/.*(github|gitlab|bitbucket)/m", $url) === 1) {
        $result = file_get_contents($url);
    }
}
```
The url must be something like : http...//....github/gitlab/bitbucket

We can see that colon(:) is not required after http (http://), so we dont need to enter a url, we can enter a path/filename as input.

It's too obvious here, we can exploit File Inclusion/Path traversal.

Flag is in `/flag.txt` and the current directory is: `/var/www/html`

![image](https://user-images.githubusercontent.com/83667873/159176250-d7cbacb2-a4c3-4b61-9d8f-d95a930b1448.png)

Okay, all we need to do now is calculate that when the values are concatenated, the value will be the path to flag.txt

I will chooses the value as below:
- service: httpa//../github
- owner=..
- repo=..
- branch=..
- file=../flag.txt

When craft_url function is called, the path ($url) will become: `httpa//../github/../../../../flag.txt` (path to flag.txt).

You can change these values to anything which when craft_url is call, it will creata valid path to flag.txt.

![image](https://user-images.githubusercontent.com/83667873/159176762-06b0e3eb-1cbe-4033-9667-115985858dd5.png)

***Flag: zer0pts{foo/bar/../../../../../directory/traversal}***

# miniblog++
