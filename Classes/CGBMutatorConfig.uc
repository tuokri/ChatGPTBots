/*
 * Copyright (c) 2025 Tuomo Kriikkula
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

class CGBMutatorConfig extends Object
    config(Mutator_ChatGPTBotsConfig)
    abstract
    notplaceable;

const CURRENT_CONFIG_VERSION = 1;
const DEFAULT_API_URL = "http://localhost:8080/api/v1/";

var() int ConfigVersion;
var() config string ApiUrl;
var() private config string ApiKey;

final function ValidateConfig()
{
    local bool bSave;

    if (ConfigVersion != CURRENT_CONFIG_VERSION)
    {
        ConfigVersion = CURRENT_CONFIG_VERSION;
        bSave = True;
    }

    if (ApiUrl == "")
    {
        ApiUrl = DEFAULT_API_URL;
        bSave = True;
    }

    if (ApiKey == "")
    {
        `cgbwarn("ApiKey is not set, features will not work!");
    }

    if (bSave)
    {
        SaveConfig();
        `cgblog("config updated");
    }
}

DefaultProperties
{
}
