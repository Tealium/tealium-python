# Tealium Library for Python

This mobile library leverages the power of Tealium's [AudienceStream™](http://tealium.com/products/audiencestream/) making it natively available to Python applications.

Please contact your Account Manager first to verify yours agreement(s) for licensed products.

### What is Audience Stream ?

Tealium AudienceStream is the leading omnichannel customer segmentation and action engine, combining robust audience management and profile enrichment capabilities with the ability to take immediate, relevant action.

AudienceStream allows you to create a unified view of your customers, correlating data across every customer touchpoint, and then leverage that comprehensive customer profile across your entire digital marketing stack.

## How To Get Started

* Check out the [Getting Started](https://community.tealiumiq.com/t5/Mobile-Libraries/Tealium-for-Python/ta-p/12496) guide for a step by step walkthrough of adding Tealium to an existing project.  
* There are many other useful articles at the [Tealium Learning Community](https://community.tealiumiq.com/).

## Contact Us

* If you have **code questions** or have experienced **errors** please post an issue in the [issues page](../../issues)
* If you have **general questions** or want to network with other users please visit the [Tealium Learning Community](https://community.tealiumiq.com)
* If you have **account specific questions** please contact your Tealium account manager

## Deprecations

- "event_name" variable is replaced by "tealium_event". Both are sent for now.

## Change Log

- 1.2.0 Support for UDH "datasource" id
   - Add "datasource" as optional argument to constructor
   - Make "environment" optional. It's no longer required, but won't break to use.

- 1.1.1 Bug Fix
   - Update track call to take named arguments

- 1.1.0
   - TrackEvent Support
   - Additional automatic data sources added to track call

- 1.0.0 Initial Release

## License

Use of this software is subject to the terms and conditions of the license agreement contained in the file titled "LICENSE.txt".  Please read the license before downloading or using any of the files contained in this repository. By downloading or using any of these files, you are agreeing to be bound by and comply with the license agreement.


---
Copyright (C) 2012-2017, Tealium Inc.
